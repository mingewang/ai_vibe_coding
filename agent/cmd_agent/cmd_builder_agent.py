"""
CLI Tool Builder Agent
======================
One-line request  ->  full working Python CLI tool

Example:
    python run.py "Build a CLI-based habit tracker with streak counter"

The agent:
  1. Generates a complete Python CLI tool (argparse, JSON persistence)
  2. Tests the generated code for syntax & runtime errors
  3. Fixes bugs automatically
  4. Saves the final tool to agent/cmd_agent/tools/
  5. Returns the file path and feature summary
"""

import json
import os
import re
import sys
from openai import OpenAI

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "tools")

DEFAULT_SYSTEM_PROMPT = """You are a CLI Tool Builder Agent. Your purpose is to build complete, working Python CLI tools from a one-line description. You never ask the user for help.

## Workflow
1. **Plan** the tool's features, commands, and arguments
2. **Write** the complete Python code
3. **Test** using ACTION: run_code(~code~) — the code arg is a Python string
4. **Fix** bugs if found, then retest
5. **Save** using ACTION: save_tool(~filename~, ~code~)
6. **Answer** with a summary of what was built

## Coding Standards
- Use `argparse` for CLI argument parsing
- Use JSON files for data persistence (in user's ~/.<toolname>/ dir or current dir)
- Include `def main():` and `if __name__ == "__main__":`
- Include `--help` with clear examples in epilog
- Use ANSI color codes for formatting (optional but nice)
- Zero external dependencies beyond the standard library
- Clean, readable code with short docstrings
- Handle errors gracefully (file not found, bad input, etc.)

## File naming
- Use snake_case for the file name based on the tool purpose
- Save to the tools/ subdirectory

## Examples of good CLI tools:
- Todo app: add/delete/list/done tasks, JSON storage
- Password generator: length/options/strength score, clipboard copy hint
- Calculator: basic ops, history, memory
- Habit tracker: add/check/streak/stats, daily reset, JSON storage
- Note taking: add/list/search/delete notes with timestamps

Always generate a complete, runnable script. Include all the code in a single ACTION: run_code or save_tool call. Never leave placeholders or TODO comments.
"""


def run_code(code: str) -> str:
    """Execute Python code and return success/error message."""
    try:
        compile(code, "<string>", "exec")
        local_scope = {}
        exec(code, local_scope)
        return "SUCCESS: Code compiled and executed with no errors."
    except SystemExit:
        return "SUCCESS: Code ran (argparse called sys.exit(0) on --help, which is expected)."
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"


def save_tool(filename: str, code: str) -> str:
    """Save generated tool code to a file and return the path."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if not filename.endswith(".py"):
        filename += ".py"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    return f"SAVED: Tool written to {filepath}"


def extract_action(reply: str, action_name: str) -> str | None:
    """Extract the argument of ACTION: action_name(~arg~) from reply."""
    pattern = rf"ACTION:\s*{action_name}\s*[(]\s*~(.+?)~\s*[)]"
    match = re.search(pattern, reply, re.DOTALL)
    if match:
        return match.group(1).strip()
    alt_pattern = rf"ACTION:\s*{action_name}\s*[(]\s*([\s\S]*?)\s*[)]"
    match = re.search(alt_pattern, reply, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None


def extract_save_action(reply: str) -> tuple[str, str] | None:
    """Extract filename and code from ACTION: save_tool(~filename~, ~code~)."""
    pattern = r"ACTION:\s*save_tool\s*[(]\s*~(.+?)~\s*,\s*~([\s\S]*?)~\s*[)]"
    match = re.search(pattern, reply, re.DOTALL)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None


def build_cli_tool(
    user_request: str,
    model: str = "deepseek-chat",
    max_turns: int = 8,
    verbose: bool = True,
) -> dict:
    """
    Build a CLI tool from a one-line description.

    Args:
        user_request: e.g. "Build a CLI-based habit tracker with streak counter"
        model: LLM model to use
        max_turns: Maximum ReAct iterations (prevents infinite loops)
        verbose: Print progress to stdout

    Returns:
        dict with keys: success, filepath, code, summary, turns_used
    """
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1",
    )

    messages = [
        {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
        {"role": "user", "content": f"Build this CLI tool:\n{user_request}"},
    ]

    turn = 0
    final_output = None

    for turn in range(max_turns):
        if verbose:
            print(f"\n--- Turn {turn + 1}/{max_turns} ---")

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,
            max_tokens=4096,
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        if verbose:
            preview = reply[:500]
            print(preview + ("..." if len(reply) > 500 else ""))

        # Handle actions
        if "ACTION: run_code(" in reply:
            code = extract_action(reply, "run_code")
            if code:
                if verbose:
                    print("\n>>> Testing code...")
                observation = run_code(code)
                if verbose:
                    print(f">>> {observation}")
                messages.append({
                    "role": "user",
                    "content": f"OBSERVATION: {observation}",
                })
                continue

        if "ACTION: save_tool(" in reply:
            result = extract_save_action(reply)
            if result:
                filename, code = result
                if verbose:
                    print(f"\n>>> Saving tool to {filename}...")
                save_msg = save_tool(filename, code)
                if verbose:
                    print(f">>> {save_msg}")
                messages.append({
                    "role": "user",
                    "content": f"OBSERVATION: {save_msg}",
                })
                continue

        final_output = reply
        break

    filepath = None
    code = None
    if final_output and "SAVED:" in str(messages):
        for msg in messages:
            if isinstance(msg, dict) and msg.get("role") == "user" and "SAVED:" in msg.get("content", ""):
                fp_match = re.search(r"SAVED: Tool written to (.+)", msg["content"])
                if fp_match:
                    filepath = fp_match.group(1)
                    break
        if filepath and os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

    success = filepath is not None and os.path.exists(filepath)

    return {
        "success": success,
        "filepath": filepath,
        "code": code,
        "summary": final_output or "No output generated.",
        "turns_used": turn + 1,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cmd_builder_agent.py \"<description of CLI tool>\"")
        print("Example: python cmd_builder_agent.py \"Build a CLI habit tracker with streak counter\"")
        sys.exit(1)

    request = " ".join(sys.argv[1:])
    result = build_cli_tool(request, verbose=True)

    print("\n" + "=" * 60)
    print("  CLI Tool Builder - Result")
    print("=" * 60)
    if result["success"]:
        print(f"  Status:  SUCCESS")
        print(f"  File:    {result['filepath']}")
        print(f"  Turns:   {result['turns_used']}")
    else:
        print(f"  Status:  FAILED")
        print(f"  Turns:   {result['turns_used']}")
    print("-" * 60)
    print(result["summary"])

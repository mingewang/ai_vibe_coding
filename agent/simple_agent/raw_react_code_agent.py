import io
import json
import os
import re
import sys
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

def run_code(code: str, test_input: str = "") -> str:
    try:
        if test_input:
            sys.stdin = io.StringIO(test_input)
        exec(code)
        return "Code ran successfully, no bugs found."
    except Exception as e:
        return f"Bug detected: {str(e)}"
    finally:
        sys.stdin = sys.__stdin__

def write_file(filepath: str, content: str) -> str:
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

TOOLS = {
    "run_code": lambda args: run_code(args["code"], args.get("test_input", "")),
    "write_file": lambda args: write_file(args["filepath"], args["content"]),
}

def extract_json(text: str) -> dict | None:
    text = re.sub(r"```[\s\S]*?```", "", text)
    idx = text.find('{"action"')
    if idx == -1:
        return None
    depth = 0
    for i in range(idx, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[idx:i+1])
    return None

def deepseek_vibe_agent(user_goal: str):
    messages = [
        {
            "role": "system",
            "content": """You are a Vibe Coding AI Agent powered by DeepSeek.
Given a user project goal:
1. Write clean, working Python code
2. Test code by returning JSON: {"action": "run_code", "code": "...", "test_input": "commands for stdin here"}
   Always include test_input to feed stdin so input() calls do not block. Simulate real usage.
3. Fix errors automatically
4. Save files by returning JSON: {"action": "write_file", "filepath": "...", "content": "..."}
5. When done, return a plain text summary of what was built
Never ask the user for help. Solve all issues yourself.
When calling a tool, return ONLY a single JSON object on its own — no markdown, no code blocks, no explanation, no surrounding text. The JSON must start with exactly: {"action":"""
        },
        {"role": "user", "content": user_goal}
    ]

    max_steps = 5
    for _ in range(max_steps):
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.1,
            max_tokens=3000
        )
        reply = response.choices[0].message.content
        print("Agent Reply:\n", reply)
        messages.append({"role": "assistant", "content": reply})

        try:
            data = extract_json(reply)
        except (ValueError, json.JSONDecodeError):
            return reply

        action = data.get("action")
        if action in TOOLS:
            result = TOOLS[action](data)
            messages.append({"role": "user", "content": f"OBSERVATION: {result}"})
        else:
            return reply
    return "Max steps reached, task completed partially."

print(deepseek_vibe_agent("Build a CLI todo list app with add/delete/view features"))

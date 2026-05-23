# Quick Start — CLI Tool Builder Agent

Turn a one-line description into a complete, working Python CLI tool.

```bash
python run.py "Build a CLI habit tracker with streak counter"
```

---

## Prerequisites

- **Python 3.10+**
- **DeepSeek API key** — set as environment variable:
  ```bash
  set DEEPSEEK_API_KEY=sk-...           # Windows cmd
  $env:DEEPSEEK_API_KEY = "sk-..."      # PowerShell
  export DEEPSEEK_API_KEY=sk-...         # macOS / Linux
  ```
- **Install dependency:**
  ```bash
  pip install openai
  ```

---

## Usage

### Build any CLI tool in one line

```bash
python run.py "Build a CLI todo list app with add/delete/list/done"
python run.py "Build a password generator with strength scoring"
python run.py "Build a CLI calculator with history and memory"
python run.py "Build a CLI note taking app with search"
python run.py "Build a CLI habit tracker with streak counter"
```

### Run the generated tool

Built tools are saved to `tools/`. Run them directly:

```bash
python tools/todo.py --help
python tools/todo.py add "Buy groceries" -p high
python tools/todo.py list
```

---

## How it works

```
You: "Build a CLI habit tracker with streak counter"
        │
        ▼
  ┌─────────────────────────────────────────────┐
  │ 1. Plan — features, commands, arguments      │
  │ 2. Write — complete Python code (argparse)   │
  │ 3. Test  — compile + exec for errors         │
  │ 4. Fix   — auto-fix bugs, retest             │
  │ 5. Save  — tools/habit_tracker.py            │
  │ 6. Done  — returns file path + summary       │
  └─────────────────────────────────────────────┘
        │
        ▼
You: python tools/habit_tracker.py --help
```

The agent uses a **ReAct loop** (Think → Act → Observe → Repeat) powered by DeepSeek. It never asks for help — it self-corrects until the tool runs.

---

## Output

Generated tools are saved under:

```
agent/cmd_agent/tools/<tool_name>.py
```

Each tool is a standalone Python script with:

- `argparse` CLI interface
- JSON file persistence (in `~/.<toolname>/` or current dir)
- `--help` with examples
- Zero external dependencies
- Error handling and colored output

---

## Example: habit tracker

```bash
python run.py "Build a CLI habit tracker with streak counter"
# → tools/habit_tracker.py

python tools/habit_tracker.py --help
python tools/habit_tracker.py add "Read 30 mins"
python tools/habit_tracker.py check 1
python tools/habit_tracker.py stats
```

---

## Programmatic use

```python
from cmd_builder_agent import build_cli_tool

result = build_cli_tool("Build a CLI password generator", verbose=True)
print(result["filepath"])   # path to saved tool
print(result["code"])       # full source code
print(result["summary"])    # agent's summary
```

---

## Notes

- Max **8 ReAct turns** per build (configurable via `max_turns` param)
- Model defaults to `deepseek-chat` (configurable via `model` param)
- Temperature is locked at **0.1** for stable code generation
- Generated tools use **only stdlib** — no extra `pip install` needed

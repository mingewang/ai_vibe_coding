import asyncio
import os
import sys
from openai import AsyncOpenAI
from agents import Agent, function_tool, ModelSettings, Runner, OpenAIChatCompletionsModel

client = AsyncOpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
)

# Define agent tools
@function_tool
def run_python_code(code: str) -> str:
    """Execute Python code and return errors/success for vibe coding debugging"""
    try:
        print("Running code:\n", code)
        exec(code)
        return "Success: Code executed with no bugs."
    except Exception as e:
        return f"Bug found: {str(e)}"

@function_tool
def write_file(filepath: str, content: str) -> str:
    """Write content to a file. Use this to save the final code and README."""
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# Build your vibe coding agent
vibe_dev_agent = Agent(
    name="CodeAgent",
    model=OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=client),
    tools=[run_python_code, write_file],
    instructions="""
You are a Vibe Coding Senior Dev Agent.
1. Understand user project requirements
2. Write clean, working Python code
3. Test code with run_python_code — set up test data yourself, never ask the user for input/output during testing
4. Fix all bugs automatically
5. Save the final complete code and a short README.md to files using write_file (use descriptive filenames like app.py, utils.py, README.md)
6. After saving, output a summary of what was built and where files were saved
Never ask the user for help—solve problems yourself.
""",
    model_settings=ModelSettings(temperature=0.1),
)

# Run autonomous project build
async def main():
    # uild a full‑featured CLI weather checker app using open‑meteo API
    prompt = sys.argv[1] if len(sys.argv) > 1 else input("Tell me what do you want to build? I will build it for you: ") 
    result = await Runner.run(vibe_dev_agent, prompt, max_turns=8)
    print(result.final_output)

asyncio.run(main())
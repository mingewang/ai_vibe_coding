import asyncio
import os
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
        print("Running code:\n", code)  # Debug log
        exec(code)
        return "Success: Code executed with no bugs."
    except Exception as e:
        return f"Bug found: {str(e)}"

# Build your vibe coding agent
vibe_dev_agent = Agent(
    name="CodeAgent",
    model=OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=client),
    tools=[run_python_code],
    instructions="""
You are a Vibe Coding Senior Dev Agent.
1. Understand user project requirements
2. Write clean, working Python code
3. Test code with run_python_code
4. Fix all bugs automatically
5. Return final complete code + short README
Never ask the user for help—solve problems yourself.
""",
    model_settings=ModelSettings(temperature=0.1),
)

# Run autonomous project build
async def main():
    result = await Runner.run(vibe_dev_agent, "Build a full‑featured CLI weather checker app using open‑meteo API", max_turns=8)
    print(result.final_output)

asyncio.run(main())
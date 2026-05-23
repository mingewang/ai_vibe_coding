import os
from openai import OpenAI

# Initialize DeepSeek client (OpenAI‑compatible)
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# Tool: Execute Python code for vibe coding debugging
def run_code(code: str) -> str:
    try:
        exec(code)
        return "✅ Code ran successfully, no bugs found."
    except Exception as e:
        return f"❌ Bug detected: {str(e)}"

# Agent execution loop: Think → Action → Observe → Answer
def deepseek_vibe_agent(user_goal: str):
    messages = [
        {
            "role": "system",
            "content": """
You are a Vibe Coding AI Agent powered by DeepSeek.
Given a user project goal:
1. Write clean, working Python code
2. Test code using ACTION: run_code(code_here)
3. Fix errors automatically
4. Return final complete working code
Do NOT ask the user for help. Solve all issues yourself.
            """
        },
        {"role": "user", "content": user_goal}
    ]

    max_steps = 5  # Prevent infinite loops (critical best practice)
    for _ in range(max_steps):
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            temperature=0.1,  # Low temp = stable code for vibe coding
            max_tokens=2000
        )
        reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        # Execute tool call
        if "ACTION: run_code(" in reply:
            code = reply.split("run_code(")[1].split(")")[0].strip()
            observation = run_code(code)
            messages.append({"role": "user", "content": f"OBSERVATION: {observation}"})
        else:
            return reply
    return "Max steps reached, task completed partially."

# Test your DeepSeek‑powered vibe coding agent
print(deepseek_vibe_agent("Build a CLI todo list app with add/delete/view features"))
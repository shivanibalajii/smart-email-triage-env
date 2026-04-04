import os
from fastapi import FastAPI
from email_environment import EmailEnvironment
from models import EmailAction
from groq import Groq

app = FastAPI(
    title="Smart Email Triage Environment",
    description="An RL environment for training agents to triage emails intelligently. Built on OpenEnv by Meta & Hugging Face.",
    version="1.0.0"
)

env = EmailEnvironment()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.get("/")
def root():
    return {"message": "Smart Email Triage Environment Running"}

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: EmailAction):
    return env.step(action)

@app.get("/history")
def history():
    return env.get_history()

@app.get("/grade")
def grade():
    h = env.get_history()
    total = sum(s["reward"] for s in h)
    correct = sum(1 for s in h if s["correct"])
    return {
        "total_reward": total,
        "correct_decisions": correct,
        "total_steps": len(h),
        "accuracy": correct / len(h) if h else 0
    }

@app.get("/grade_llm")
def grade_llm():
    h = env.get_history()
    if not h:
        return {"error": "No history yet. Call /reset and /step first."}

    history_text = "\n".join([
        f"Email: '{s['email_subject']}' | Correct: {s['correct_action']} | Agent did: {s['agent_action']} | Reward: {s['reward']}"
        for s in h
    ])

    prompt = f"""You are evaluating an AI agent that triages emails.
The agent can take 4 actions: reply, escalate, archive, flag.

Here is the agent's episode history:
{history_text}

Please evaluate:
1. Did the agent correctly prioritize urgent emails?
2. Did it correctly flag security threats?
3. Did it avoid unnecessary escalations?
4. Overall score out of 10 and brief feedback.

Keep your response concise."""

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return {
        "llm_evaluation": response.choices[0].message.content,
        "rule_based_accuracy": sum(1 for s in h if s["correct"]) / len(h) if h else 0,
        "total_reward": sum(s["reward"] for s in h)
    }
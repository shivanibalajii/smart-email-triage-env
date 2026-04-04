from fastapi import FastAPI
from server.email_environment import EmailEnvironment
from models import EmailAction

app = FastAPI()
env = EmailEnvironment()

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
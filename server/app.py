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
    if not h:
        return {
            "total_reward": 0.5,
            "correct_decisions": 0,
            "total_steps": 0,
            "accuracy": 0.5,
            "score": 0.5
        }
    total = sum(s["reward"] for s in h)
    correct = sum(1 for s in h if s["correct"])
    raw_accuracy = correct / len(h)
    raw_score = total / len(h)
    return {
        "total_reward": round(min(0.99, max(0.01, total / len(h))), 3),
        "correct_decisions": correct,
        "total_steps": len(h),
        "accuracy": round(min(0.99, max(0.01, raw_accuracy)), 3),
        "score": round(min(0.99, max(0.01, raw_score)), 3)
    }
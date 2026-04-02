from fastapi import FastAPI

app = FastAPI()

emails = [
    {"subject": "Team Meeting Reminder", "sender": "team"},
    {"subject": "URGENT: Production Server Down", "sender": "boss"},
    {"subject": "Weekly Report Submission", "sender": "team"},
]

@app.post("/reset")
def reset():
    return {"message": "Environment reset successful"}

@app.get("/")
def root():
    return {"message": "Smart Email Triage Env is running"}

@app.post("/step")
def step():
    results = []
    score = 0

    for email in emails:
        if "URGENT" in email["subject"] or email["sender"] == "boss":
            action = "escalate"
            reward = 1.0
        else:
            action = "reply"
            reward = 0.8

        score += reward

        results.append({
            "email": email,
            "action": action,
            "reward": reward
        })

    return {
        "results": results,
        "final_score": score
    }

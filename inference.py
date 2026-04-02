from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Simple state
emails = []
current_index = 0

class StepInput(BaseModel):
    action: str

@app.post("/reset")
def reset():
    global emails, current_index

    emails = [
        {"subject": "Team Meeting Reminder", "sender": "team"},
        {"subject": "URGENT: Production Server Down", "sender": "boss"},
        {"subject": "Weekly Report Submission", "sender": "team"}
    ]
    current_index = 0

    return {
        "observation": emails[current_index],
        "reward": 0,
        "done": False
    }

@app.post("/step")
def step(input: StepInput):
    global current_index

    reward = 0

    # simple logic
    if "urgent" in emails[current_index]["subject"].lower():
        if input.action == "escalate":
            reward = 1
    else:
        if input.action == "reply":
            reward = 1

    current_index += 1

    done = current_index >= len(emails)

    observation = emails[current_index] if not done else {}

    return {
        "observation": observation,
        "reward": reward,
        "done": done
    }

@app.get("/")
def home():
    return {"status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

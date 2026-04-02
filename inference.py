from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

emails = []
current_index = 0
step_count = 0

class ActionInput(BaseModel):
    action_type: str
    email_index: int

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    global emails, current_index, step_count

    emails = [
        {"subject": "Team Meeting Reminder", "sender": "team", "body": "Meeting at 10 AM", "priority": 2},
        {"subject": "URGENT: Production Server Down", "sender": "boss", "body": "Fix immediately", "priority": 3},
        {"subject": "Weekly Report Submission", "sender": "team", "body": "Submit by EOD", "priority": 2}
    ]

    current_index = 0
    step_count = 0

    return {
        "observation": {
            "emails": emails,
            "step_count": step_count
        }
    }

@app.post("/step")
def step(input: ActionInput):
    global current_index, emails, step_count

    if current_index >= len(emails):
        return {
            "observation": {
                "emails": emails,
                "step_count": step_count
            },
            "reward": 0.0,
            "done": True,
            "info": {}
        }

    email = emails[current_index]

    # reward logic
    if email["sender"] == "boss":
        reward = 1.0 if input.action_type == "escalate" else -1.0
    elif email["sender"] == "team":
        reward = 0.8 if input.action_type == "reply" else -0.3
    else:
        reward = 0.5 if input.action_type == "ignore" else -0.2

    current_index += 1
    step_count += 1

    done = current_index >= len(emails)

    return {
        "observation": {
            "emails": emails,
            "step_count": step_count
        },
        "reward": reward,
        "done": done,
        "info": {}
    }
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Global state
emails = []
current_index = 0


class ActionInput(BaseModel):
    action: str


@app.get("/")
def home():
    return {"status": "ok"}


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
        "observation": {
            "subject": emails[0]["subject"],
            "sender": emails[0]["sender"]
        },
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
def step(input: ActionInput):
    global current_index, emails

    # If already finished
    if current_index >= len(emails):
        return {
            "observation": {},
            "reward": 0.0,
            "done": True,
            "info": {}
        }

    email = emails[current_index]

    # Reward logic
    if "urgent" in email["subject"].lower():
        reward = 1.0 if input.action == "escalate" else 0.0
    else:
        reward = 1.0 if input.action == "reply" else 0.0

    current_index += 1
    done = current_index >= len(emails)

    observation = (
        {
            "subject": emails[current_index]["subject"],
            "sender": emails[current_index]["sender"]
        }
        if not done else {}
    )

    return {
        "observation": observation,
        "reward": reward,
        "done": done,
        "info": {}
    }
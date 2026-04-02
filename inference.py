from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

    try:
        emails = [
            {"subject": "Team Meeting Reminder", "sender": "team"},
            {"subject": "URGENT: Production Server Down", "sender": "boss"},
            {"subject": "Weekly Report Submission", "sender": "team"}
        ]

        current_index = 0

        return {
            "observation": emails[0],
            "reward": 0,
            "done": False
        }

    except Exception as e:
        return {
            "observation": {},
            "reward": 0,
            "done": True,
            "error": str(e)
        }

@app.post("/step")
def step(input: ActionInput):
    global current_index, emails

    try:
        if current_index >= len(emails):
            return {
                "observation": {},
                "reward": 0,
                "done": True
            }

        email = emails[current_index]

        if "urgent" in email["subject"].lower():
            reward = 1 if input.action == "escalate" else 0
        else:
            reward = 1 if input.action == "reply" else 0

        current_index += 1
        done = current_index >= len(emails)

        observation = emails[current_index] if not done else {}

        return {
            "observation": observation,
            "reward": reward,
            "done": done
        }

    except Exception as e:
        return {
            "observation": {},
            "reward": 0,
            "done": True,
            "error": str(e)
        }
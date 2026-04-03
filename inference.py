from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

# GLOBAL STATE
emails = []
current_index = 0

# REQUEST MODEL
class ActionInput(BaseModel):
    action: str


# ✅ RESET ENDPOINT
@app.post("/reset")
def reset():
    global emails, current_index

    print("START")  # REQUIRED LOG

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


# ✅ STEP ENDPOINT
@app.post("/step")
def step(input: ActionInput):
    global current_index, emails

    print("STEP")  # REQUIRED LOG

    if current_index >= len(emails):
        print("END")
        return {
            "observation": {},
            "reward": 0.0,
            "done": True,
            "info": {}
        }

    email = emails[current_index]

    # SIMPLE LOGIC
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

    if done:
        print("END")  # REQUIRED LOG

    return {
        "observation": observation,
        "reward": reward,
        "done": done,
        "info": {}
    }
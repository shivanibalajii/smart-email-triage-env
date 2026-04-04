from fastapi import FastAPI
from server.email_environment import EmailEnvironment
from models import EmailAction

app = FastAPI()

# Initialize environment
env = EmailEnvironment()


# ROOT (optional)

@app.get("/")
def root():
    return {"message": "Smart Email Triage Environment Running"}


# RESET (start new episode)

@app.post("/reset")
def reset():
    return env.reset()

# STEP (agent takes action)

@app.post("/step")
def step(action: EmailAction):
    return env.step(action)
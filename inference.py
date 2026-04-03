from fastapi import FastAPI

app = FastAPI()

# -----------------------------
# REQUIRED ENV VARIABLES
# -----------------------------
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

# -----------------------------
# GLOBAL STATE
# -----------------------------
emails = []

# -----------------------------
# ROOT (optional)
# -----------------------------
@app.get("/")
def root():
    return {"message": "API running"}

# -----------------------------
# RESET ENDPOINT (VERY IMPORTANT)
# -----------------------------
@app.post("/reset")
def reset():
    global emails
    emails = []
    return {"status": "reset successful"}

# -----------------------------
# SAMPLE PROCESS ENDPOINT
# -----------------------------
@app.post("/process")
def process_email(data: dict):
    global emails

    email = data.get("email")
    if email:
        emails.append(email)

    return {
        "message": "email received",
        "total_emails": len(emails)
    }
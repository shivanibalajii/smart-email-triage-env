import os
import json
import random
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
API_KEY = os.environ.get("API_KEY", os.environ.get("HF_TOKEN", "dummy"))

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
app = FastAPI(title="Smart Email Triage Environment")

class Action(BaseModel):
    action: str

class Observation(BaseModel):
    email_id: int
    subject: str
    sender: str
    body: str
    task: str
    difficulty: str

class Reward(BaseModel):
    reward: float
    correct: bool
    true_label: str

TASKS = {
    "easy": {
        "description": "Classify obviously spam or urgent emails",
        "emails": [
            {"id": 1, "subject": "Win a FREE iPhone now!", "body": "Click here to claim your prize!", "sender": "promo@spam.com", "label": "archive"},
            {"id": 2, "subject": "URGENT: Production server is down", "body": "Our main server crashed. Revenue loss every minute.", "sender": "ops@company.com", "label": "escalate"},
            {"id": 3, "subject": "Congratulations! You won $1,000,000", "body": "Send us your bank details.", "sender": "lottery@scam.com", "label": "archive"},
            {"id": 4, "subject": "CRITICAL: Database breach detected", "body": "Unauthorized access to customer data.", "sender": "security@company.com", "label": "escalate"},
            {"id": 5, "subject": "FREE vacation giveaway", "body": "You have been selected for a free cruise!", "sender": "promo@fake.com", "label": "archive"},
        ]
    },
    "medium": {
        "description": "Classify emails requiring context awareness",
        "emails": [
            {"id": 6, "subject": "Suspicious login from unknown device", "body": "Someone logged into your account from Russia.", "sender": "security@bank.com", "label": "flag"},
            {"id": 7, "subject": "Invoice #4521 attached", "body": "Please find the invoice for last month.", "sender": "billing@vendor.com", "label": "reply"},
            {"id": 8, "subject": "URGENT: CEO needs wire transfer", "body": "Transfer $50,000 immediately. Keep it secret.", "sender": "ceo.fake@gmail.com", "label": "flag"},
            {"id": 9, "subject": "Meeting rescheduled to 3pm", "body": "Moving our sync to 3pm today.", "sender": "manager@company.com", "label": "reply"},
            {"id": 10, "subject": "Phishing link detected in email", "body": "Our system flagged a malicious URL sent to all staff.", "sender": "it@company.com", "label": "flag"},
        ]
    },
    "hard": {
        "description": "Classify ambiguous emails needing nuanced judgment",
        "emails": [
            {"id": 11, "subject": "Your account password", "body": "Click this link to verify your bank password immediately.", "sender": "noreply@phish.com", "label": "flag"},
            {"id": 12, "subject": "Server CPU at 98%", "body": "Automated alert: CPU usage critical on prod-server-01.", "sender": "monitoring@company.com", "label": "escalate"},
            {"id": 13, "subject": "Verify your email address", "body": "Click to verify your account on our platform.", "sender": "no-reply@legit.com", "label": "reply"},
            {"id": 14, "subject": "Ransomware detected on workstation", "body": "Workstation WS-042 infected. Disconnect immediately.", "sender": "security@company.com", "label": "escalate"},
            {"id": 15, "subject": "Unusual API activity detected", "body": "10,000 failed login attempts on your API in the last hour.", "sender": "security@api.com", "label": "flag"},
        ]
    }
}

REWARD_MAP = {
    ("escalate", "escalate"): 0.95,
    ("flag", "flag"): 0.95,
    ("reply", "reply"): 0.95,
    ("archive", "archive"): 0.95,
    ("escalate", "archive"): 0.05,
    ("escalate", "reply"): 0.05,
    ("escalate", "flag"): 0.30,
    ("flag", "archive"): 0.05,
    ("flag", "reply"): 0.05,
    ("flag", "escalate"): 0.30,
    ("archive", "escalate"): 0.15,
    ("reply", "escalate"): 0.15,
}

def get_reward(true_label, action):
    base = REWARD_MAP.get((true_label, action), 0.15)
    noise = round(random.uniform(-0.03, 0.03), 3)
    return round(min(0.99, max(0.01, base + noise)), 3)

state = {
    "task": "easy",
    "emails": [],
    "current_index": 0,
    "history": [],
    "total_reward": 0.0,
    "correct": 0,
}

@app.post("/reset")
def reset(task: str = "easy"):
    if task not in TASKS:
        task = "easy"
    emails = TASKS[task]["emails"].copy()
    random.shuffle(emails)
    state["task"] = task
    state["emails"] = emails
    state["current_index"] = 0
    state["history"] = []
    state["total_reward"] = 0.0
    state["correct"] = 0
    first = emails[0]
    return Observation(
        email_id=first["id"],
        subject=first["subject"],
        sender=first["sender"],
        body=first["body"],
        task=task,
        difficulty=task,
    )

class StepRequest(BaseModel):
    action: str

@app.post("/step")
def step(req: StepRequest):
    idx = state["current_index"]
    if idx >= len(state["emails"]):
        return {"done": True, "message": "Episode complete. Call /reset to start again."}
    email = state["emails"][idx]
    action = req.action.strip().lower()
    true_label = email["label"]
    reward = get_reward(true_label, action)
    correct = action == true_label
    state["total_reward"] += reward
    if correct:
        state["correct"] += 1
    state["history"].append({
        "email_id": email["id"],
        "subject": email["subject"],
        "action": action,
        "true_label": true_label,
        "reward": reward,
        "correct": correct,
    })
    state["current_index"] += 1
    done = state["current_index"] >= len(state["emails"])
    obs = None if done else state["emails"][state["current_index"]]
    return {
        "observation": None if done else Observation(
            email_id=obs["id"],
            subject=obs["subject"],
            sender=obs["sender"],
            body=obs["body"],
            task=state["task"],
            difficulty=state["task"],
        ).dict(),
        "reward": Reward(reward=reward, correct=correct, true_label=true_label).dict(),
        "done": done,
        "info": {"step": idx + 1, "total": len(state["emails"])},
    }

@app.get("/state")
def get_state():
    return {
        "task": state["task"],
        "current_index": state["current_index"],
        "total_emails": len(state["emails"]),
        "total_reward": round(state["total_reward"], 3),
        "correct": state["correct"],
        "accuracy": round(state["correct"] / max(1, state["current_index"]), 3),
    }

@app.get("/history")
def history():
    return {"history": state["history"]}

@app.get("/grade")
def grade():
    total = len(state["history"])
    if total == 0:
        return {"message": "No episode run yet. Call /reset then /step."}
    return {
        "task": state["task"],
        "total_emails": total,
        "correct": state["correct"],
        "accuracy": round(min(0.99, max(0.01, state["correct"] / total)), 3),
        "total_reward": round(state["total_reward"], 3),
        "score": round(min(0.99, max(0.01, state["total_reward"] / total)), 3),
    }

@app.get("/grade_llm")
def grade_llm():
    if not state["history"]:
        return {"message": "No episode run yet."}
    try:
        summary = json.dumps(state["history"][:5], indent=2)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert evaluator of email triage agents. Given a sample of decisions, evaluate the agent's reasoning quality in 2-3 sentences."},
                {"role": "user", "content": f"Here are the agent's decisions:\n{summary}\nEvaluate the quality of these decisions."}
            ],
            max_tokens=300,
        )
        evaluation = response.choices[0].message.content.strip()
        return {
            "task": state["task"],
            "score": round(min(0.99, max(0.01, state["total_reward"] / max(1, len(state["history"])))), 3),
            "llm_evaluation": evaluation,
        }
    except Exception as e:
        return {"error": str(e)}

def run_task(task_name):
    emails = TASKS[task_name]["emails"].copy()
    random.shuffle(emails)
    total_reward = 0.0
    correct = 0
    for step_num, email in enumerate(emails, 1):
        task_id = f"{task_name}_email_{email['id']}"
        print(f"[START] task={task_id}", flush=True)
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an email triage agent. Classify the email as one of: escalate, reply, archive, flag. Reply with ONLY the single word."},
                    {"role": "user", "content": f"Subject: {email['subject']}\nFrom: {email['sender']}\nBody: {email['body']}"}
                ],
                max_tokens=10,
            )
            action = response.choices[0].message.content.strip().lower()
            if action not in ("escalate", "reply", "archive", "flag"):
                action = "reply"
        except Exception:
            action = "reply"
        reward = get_reward(email["label"], action)
        total_reward += reward
        if action == email["label"]:
            correct += 1
        print(f"[STEP] step={step_num} action={action} true_label={email['label']} reward={reward}", flush=True)
    score = round(min(0.99, max(0.01, total_reward / len(emails))), 3)
    print(f"[END] task={task_name} score={score} steps={len(emails)}", flush=True)
    return score

def run_agent():
    scores = {}
    for task_name in ["easy", "medium", "hard"]:
        scores[task_name] = run_task(task_name)
    overall = round(min(0.99, max(0.01, sum(scores.values()) / len(scores))), 3)
    print(f"[END] task=smart_email_triage score={overall} steps={sum(len(TASKS[t]['emails']) for t in TASKS)}", flush=True)

if __name__ == "__main__":
    run_agent()
import os
import sys
import json
import random
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
API_KEY = os.environ.get("API_KEY", os.environ.get("HF_TOKEN", "dummy"))

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)

app = FastAPI(title="Smart Email Triage Environment")

EMAILS = [
    {"id": 1, "subject": "URGENT: Production server is down", "body": "Our main server crashed. Revenue loss every minute.", "sender": "ops@company.com", "label": "escalate"},
    {"id": 2, "subject": "Win a FREE iPhone now!", "body": "Click here to claim your prize!", "sender": "promo@spam.com", "label": "archive"},
    {"id": 3, "subject": "Suspicious login from unknown device", "body": "Someone logged into your account from Russia.", "sender": "security@bank.com", "label": "flag"},
    {"id": 4, "subject": "Team lunch tomorrow?", "body": "Hey, are you free for lunch at 1pm?", "sender": "friend@example.com", "label": "reply"},
    {"id": 5, "subject": "CRITICAL: Database breach detected", "body": "Unauthorized access to customer data detected now.", "sender": "security@company.com", "label": "escalate"},
    {"id": 6, "subject": "Your account password", "body": "Click this link to verify your bank password immediately.", "sender": "noreply@phish.com", "label": "flag"},
    {"id": 7, "subject": "Invoice #4521 attached", "body": "Please find attached the invoice for last month.", "sender": "billing@vendor.com", "label": "reply"},
    {"id": 8, "subject": "Congratulations! You won $1,000,000", "body": "Send us your bank details to claim your winnings.", "sender": "lottery@scam.com", "label": "archive"},
    {"id": 9, "subject": "URGENT: CEO needs wire transfer", "body": "This is the CEO. Transfer $50,000 immediately. Keep it secret.", "sender": "ceo.fake@gmail.com", "label": "flag"},
    {"id": 10, "subject": "Meeting rescheduled to 3pm", "body": "Hi, moving our sync to 3pm today instead of 2pm.", "sender": "manager@company.com", "label": "reply"},
    {"id": 11, "subject": "Server CPU at 98% — alert", "body": "Automated alert: CPU usage critical on prod-server-01.", "sender": "monitoring@company.com", "label": "escalate"},
    {"id": 12, "subject": "Newsletter: Top 10 AI trends", "body": "This week in AI: GPT-5, robotics, and more.", "sender": "newsletter@techblog.com", "label": "archive"},
    {"id": 13, "subject": "Your prescription is ready", "body": "Your medication is ready for pickup at CVS.", "sender": "cvs@pharmacy.com", "label": "reply"},
    {"id": 14, "subject": "URGENT: Legal action pending", "body": "You must respond to this legal notice within 24 hours.", "sender": "legal@company.com", "label": "escalate"},
    {"id": 15, "subject": "Phishing link detected in email", "body": "Our system flagged an email with a malicious URL sent to all staff.", "sender": "it@company.com", "label": "flag"},
    {"id": 16, "subject": "Happy Birthday!", "body": "Wishing you a wonderful birthday!", "sender": "friend@gmail.com", "label": "reply"},
    {"id": 17, "subject": "50% off sale this weekend only", "body": "Shop now and save big this weekend!", "sender": "deals@store.com", "label": "archive"},
    {"id": 18, "subject": "Data center fire — evacuate now", "body": "Emergency: fire alarm triggered in server room B.", "sender": "facilities@company.com", "label": "escalate"},
    {"id": 19, "subject": "Verify your email address", "body": "Click to verify your account on our platform.", "sender": "no-reply@legit.com", "label": "reply"},
    {"id": 20, "subject": "Ransomware detected on workstation", "body": "Workstation WS-042 is infected. Disconnect from network immediately.", "sender": "security@company.com", "label": "flag"},
    {"id": 21, "subject": "Project deadline moved up", "body": "Client wants delivery by Friday instead of next week.", "sender": "pm@company.com", "label": "reply"},
    {"id": 22, "subject": "Free vacation giveaway", "body": "You have been selected for a free cruise. Claim now!", "sender": "promo@fakevacation.com", "label": "archive"},
    {"id": 23, "subject": "URGENT: Payment gateway is down", "body": "Customers cannot checkout. Fix immediately.", "sender": "ecommerce@company.com", "label": "escalate"},
    {"id": 24, "subject": "Unusual API activity detected", "body": "10,000 failed login attempts on your API in the last hour.", "sender": "security@api.com", "label": "flag"},
    {"id": 25, "subject": "Can you review my PR?", "body": "Hey, could you review pull request #142 when you get a chance?", "sender": "dev@company.com", "label": "reply"},
]

REWARD_MAP = {
    ("escalate", "escalate"): 2.0,
    ("flag", "flag"): 1.5,
    ("reply", "reply"): 1.0,
    ("archive", "archive"): 1.0,
    ("escalate", "archive"): -2.0,
    ("escalate", "reply"): -2.0,
    ("escalate", "flag"): -0.5,
    ("flag", "archive"): -1.5,
    ("flag", "reply"): -1.5,
    ("flag", "escalate"): -0.5,
    ("archive", "escalate"): -1.0,
    ("reply", "escalate"): -1.0,
}

state = {
    "emails": [],
    "current_index": 0,
    "history": [],
    "total_reward": 0.0,
    "correct": 0,
}

def get_reward(true_label, action):
    return REWARD_MAP.get((true_label, action), -0.5)

@app.post("/reset")
def reset():
    emails = EMAILS.copy()
    random.shuffle(emails)
    state["emails"] = emails
    state["current_index"] = 0
    state["history"] = []
    state["total_reward"] = 0.0
    state["correct"] = 0
    first = state["emails"][0]
    return {
        "email_id": first["id"],
        "subject": first["subject"],
        "body": first["body"],
        "sender": first["sender"],
        "remaining": len(state["emails"]),
    }

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
    if done:
        return {
            "done": True,
            "reward": reward,
            "total_reward": state["total_reward"],
            "accuracy": round(state["correct"] / len(state["emails"]) * 100, 1),
        }
    next_email = state["emails"][state["current_index"]]
    return {
        "done": False,
        "reward": reward,
        "total_reward": state["total_reward"],
        "next_email": {
            "email_id": next_email["id"],
            "subject": next_email["subject"],
            "body": next_email["body"],
            "sender": next_email["sender"],
        },
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
        "total_emails": total,
        "correct": state["correct"],
        "accuracy": round(state["correct"] / total * 100, 1),
        "total_reward": round(state["total_reward"], 2),
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
            "accuracy": round(state["correct"] / len(state["history"]) * 100, 1),
            "total_reward": round(state["total_reward"], 2),
            "llm_evaluation": evaluation,
        }
    except Exception as e:
        return {"error": str(e)}

def run_agent():
    emails = EMAILS.copy()
    random.shuffle(emails)
    total_reward = 0.0
    correct = 0

    for step_num, email in enumerate(emails, 1):
        task_id = f"email_{email['id']}"
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

    score = round(correct / len(emails), 2)
    print(f"[END] task=smart_email_triage score={score} steps={len(emails)}", flush=True)

if __name__ == "__main__":
    run_agent()
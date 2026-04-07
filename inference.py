import os
import sys
import json
import time


from openai import OpenAI


MODEL_NAME = os.environ.get("MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
HF_TOKEN   = os.environ.get("HF_TOKEN", "")

client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1/",
    api_key=HF_TOKEN,
)

def log_start(task_id, task_input):
    print(json.dumps({
        "event": "START",
        "task_id": task_id,
        "input": task_input
    }), flush=True)

def log_step(task_id, step_name, details):
    print(json.dumps({
        "event": "STEP",
        "task_id": task_id,
        "step": step_name,
        "details": details
    }), flush=True)

def log_end(task_id, output, success=True):
    print(json.dumps({
        "event": "END",
        "task_id": task_id,
        "output": output,
        "success": success
    }), flush=True)


def run_agent():
    
    tasks = [
        {
            "id": "task_001",
            "email_subject": "Urgent: Server is down",
            "email_body": "Our production server is not responding since 2am.",
            "email_sender": "ops@company.com"
        },
        {
            "id": "task_002",
            "email_subject": "Team lunch tomorrow?",
            "email_body": "Hey, are you free for lunch tomorrow at 1pm?",
            "email_sender": "friend@example.com"
        },
    ]

    for task in tasks:
        task_id = task["id"]
        log_start(task_id, task)

        try:
            log_step(task_id, "llm_call", {"model": MODEL_NAME})

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an email triage assistant. "
                            "Classify each email into one of: URGENT, NORMAL, LOW_PRIORITY, SPAM. "
                            "Also provide a 1-sentence summary. "
                            "Respond ONLY as JSON: {\"category\": \"...\", \"summary\": \"...\"}"
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Subject: {task['email_subject']}\n"
                            f"From: {task['email_sender']}\n"
                            f"Body: {task['email_body']}"
                        )
                    }
                ],
                max_tokens=200,
            )

            raw = response.choices[0].message.content.strip()
            log_step(task_id, "llm_response", {"raw": raw})

            
            try:
                result = json.loads(raw)
            except json.JSONDecodeError:
                result = {"raw_output": raw}

            log_end(task_id, result, success=True)

        except Exception as e:
            # ✅ Wrap ALL risky ops in try/except — validator requirement
            log_step(task_id, "error", {"error": str(e)})
            log_end(task_id, {"error": str(e)}, success=False)

if __name__ == "__main__":
    run_agent()
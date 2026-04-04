"""
Smart Email Triage - Inference Script
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI

IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
TASK_NAME = "email-triage"
BENCHMARK = "smart-email-triage"
MAX_STEPS = 25

SYSTEM_PROMPT = textwrap.dedent("""
    You are an intelligent email triage agent.
    You will be shown one email at a time and must decide what to do with it.
    
    Your options are:
    - reply: for normal emails that need a response
    - escalate: for urgent emails needing immediate human attention
    - archive: for spam, newsletters, or irrelevant emails
    - flag: for suspicious emails, phishing attempts, or security threats
    
    Respond with exactly one word: reply, escalate, archive, or flag.
    Nothing else. Just the single action word.
""").strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)


def get_decision(client: OpenAI, email_subject: str, email_sender: str, email_body: str) -> str:
    user_prompt = textwrap.dedent(f"""
        Email details:
        Subject: {email_subject}
        From: {email_sender}
        Body: {email_body}
        
        What is your decision? Reply with one word only: reply, escalate, archive, or flag.
    """).strip()

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            max_tokens=10,
            stream=False,
        )
        decision = (completion.choices[0].message.content or "").strip().lower()
        if decision not in ["reply", "escalate", "archive", "flag"]:
            decision = "reply"
        return decision
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "reply"


import requests

BASE_URL = "http://localhost:7860"


def reset_env():
    response = requests.post(f"{BASE_URL}/reset")
    return response.json()


def step_env(email_id: str, decision: str):
    response = requests.post(f"{BASE_URL}/step", json={
        "email_id": email_id,
        "decision": decision
    })
    return response.json()


def grade_env():
    response = requests.get(f"{BASE_URL}/grade")
    return response.json()


async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    rewards: List[float] = []
    steps_taken = 0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        obs = reset_env()
        done = obs.get("done", False)

        step = 1
        while not done and step <= MAX_STEPS:
            email_id = obs.get("email_id", str(step))
            email_subject = obs.get("email_subject", "")
            email_sender = obs.get("email_sender", "")
            email_body = obs.get("email_body", "")

            decision = get_decision(client, email_subject, email_sender, email_body)

            obs = step_env(email_id, decision)
            reward = obs.get("reward", 0.0)
            done = obs.get("done", False)
            error = None

            rewards.append(reward)
            steps_taken = step

            log_step(step=step, action=decision, reward=reward, done=done, error=error)

            step += 1

        grade = grade_env()
        accuracy = grade.get("accuracy", 0.0)
        success = accuracy >= 0.5

    except Exception as e:
        print(f"[DEBUG] Error: {e}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())
import os
import textwrap
from typing import List, Optional

from fastapi import FastAPI
from email_environment import EmailEnvironment
from models import EmailAction

app = FastAPI(
    title="Smart Email Triage Environment",
    description="An RL environment for training agents to triage emails intelligently. Built on OpenEnv by Meta & Hugging Face.",
    version="1.0.0"
)

env = EmailEnvironment()

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
TASK_NAME = "email-triage"
BENCHMARK = "smart-email-triage"

@app.get("/")
def root():
    return {"message": "Smart Email Triage Environment Running"}

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: EmailAction):
    return env.step(action)

@app.get("/history")
def history():
    return env.get_history()

@app.get("/grade")
def grade():
    h = env.get_history()
    total = sum(s["reward"] for s in h)
    correct = sum(1 for s in h if s["correct"])
    return {
        "total_reward": total,
        "correct_decisions": correct,
        "total_steps": len(h),
        "accuracy": correct / len(h) if h else 0
    }

def log_start(task: str, env_name: str, model: str) -> None:
    print(f"[START] task={task} env={env_name} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", flush=True)

def log_end(success: bool, steps: int, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)

def run_agent():
    from openai import OpenAI
    import requests

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    BASE_URL = "http://localhost:7860"

    SYSTEM_PROMPT = textwrap.dedent("""
        You are an intelligent email triage agent.
        You will be shown one email at a time and must decide what to do with it.
        Your options are: reply, escalate, archive, flag.
        Respond with exactly one word only.
    """).strip()

    rewards: List[float] = []
    steps_taken = 0
    success = False

    log_start(task=TASK_NAME, env_name=BENCHMARK, model=MODEL_NAME)

    try:
        obs = requests.post(f"{BASE_URL}/reset").json()
        done = obs.get("done", False)
        step = 1

        while not done and step <= 25:
            user_prompt = f"Subject: {obs.get('email_subject','')}\nFrom: {obs.get('email_sender','')}\nBody: {obs.get('email_body','')}\nDecision?"

            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=0.1,
                    max_tokens=10,
                )
                decision = (completion.choices[0].message.content or "").strip().lower()
                if decision not in ["reply", "escalate", "archive", "flag"]:
                    decision = "reply"
            except Exception as e:
                print(f"[DEBUG] LLM error: {e}", flush=True)
                decision = "reply"

            obs = requests.post(f"{BASE_URL}/step", json={
                "email_id": obs.get("email_id", str(step)),
                "decision": decision
            }).json()

            reward = obs.get("reward", 0.0)
            done = obs.get("done", False)
            rewards.append(reward)
            steps_taken = step
            log_step(step=step, action=decision, reward=reward, done=done, error=None)
            step += 1

        grade = requests.get(f"{BASE_URL}/grade").json()
        success = grade.get("accuracy", 0.0) >= 0.5

    except Exception as e:
        print(f"[DEBUG] Error: {e}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, rewards=rewards)


if __name__ == "__main__":
    run_agent()
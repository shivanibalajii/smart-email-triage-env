# Smart Email Triage Environment

I built this as a small experiment to simulate how an agent could handle emails based on priority.

The idea is simple: emails come in, and the system decides what to do with them (reply, escalate, etc.) while getting a reward based on whether the decision makes sense.

---

## What it does

- Takes a few sample emails
- Looks at things like subject and sender
- Chooses an action (reply / escalate)
- Assigns a reward based on that decision
- Calculates a final score

It’s not a full RL model yet, more like a clean environment setup that could later be used to plug in a learning algorithm.

---

## Why I made this

Email overload is a real problem, especially in work settings. Not everything needs the same level of attention.

I wanted to explore how a system could:
- prioritize urgent emails
- avoid unnecessary escalation
- make consistent decisions

This is a small step toward that.

---

## How it works

The current logic is rule-based:
- Emails marked “URGENT” or from a boss → escalate
- Everything else → reply

Each action gets a reward, and the total score reflects how well the system performed.
update for validation

---

## Running it locally

```bash
python inference.py

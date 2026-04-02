# 📧 Email Triage Environment (OpenEnv)

## What this is

This project is a simple simulation of something we deal with every day — managing emails.

The idea is to model how an AI assistant could go through a set of emails and decide what to do with each one:
- reply to it  
- ignore it  
- or escalate it if it’s important  

Instead of building a full AI system, I focused on building the **environment** where an agent can learn and be evaluated.

---

## Why this matters

In real life, inboxes get messy fast. Important emails can be missed, and low-value ones waste time.

This environment tries to capture that problem in a clean way:
- some emails are critical  
- some are normal  
- some are just noise  

The goal is to take the right action for each.

---

## How the environment works

The environment follows a simple loop:

- `reset()` → generates a fresh set of emails  
- `step(action)` → applies an action and returns a reward  
- `state()` → shows the current progress  

Each run contains a small batch of emails, and the agent processes them one by one.

---

## What an email looks like

Each email has:
- subject  
- body  
- sender (boss, team, or spam)  
- priority (1–3)

The emails are slightly randomized every time, so it doesn’t feel like a fixed toy example.

---

## Actions

For each email, the agent can choose:

- `reply`  
- `ignore`  
- `escalate`  

---

## Reward logic (how scoring works)

The reward system is designed to feel realistic:

- Boss emails → should be escalated  
- Team emails → should be replied to  
- Spam → should be ignored  

Correct actions give positive rewards.  
Wrong actions give penalties, and mistakes on important emails are punished more.

Example:
- Correct boss handling → +1.0  
- Wrong boss handling → -1.0  
- Spam handled correctly → +0.5  

This makes the agent prioritize properly instead of treating everything the same.

---

## Difficulty levels

The environment is designed with increasing complexity:

- Easy → just identify spam vs important  
- Medium → choose correct action per email  
- Hard → handle multiple emails with priority  

---

## Running the project

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
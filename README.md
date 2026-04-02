# 📧 Email Triage Environment

Built as part of an OpenEnv environment design challenge.

## What I built

I tried to model something simple but real — how we deal with emails.

Instead of just classifying emails, the environment simulates actually taking actions on them. For each email, the agent has to decide whether to reply, ignore, or escalate it.

---

## Why this idea

Email overload is something everyone deals with. Important emails get missed, and a lot of time goes into handling things that don’t really matter.

So the goal here was to create a small environment where an agent can learn to make better decisions based on priority.

---

## How it works

Each run generates a small set of emails. Every email has:
- a subject  
- a body  
- a sender (boss, team, or spam)  
- a priority level  

The agent processes them one by one.

At every step:
- it picks an action  
- the environment gives a reward  
- and moves forward  

---

## Actions

The agent can choose:
- reply  
- ignore  
- escalate  

---

## Reward logic

I tried to keep the rewards realistic instead of uniform.

- Boss emails → should be escalated  
- Team emails → should be replied to  
- Spam → should be ignored  

Mistakes on important emails are penalized more than smaller mistakes.

The idea was to make the agent actually care about priority, not just accuracy.

---

## Small details I added

- Emails are slightly randomized every run so it’s not fixed  
- The reward system isn’t binary — it gives partial credit  
- The environment runs step-by-step instead of all at once  

---

## Running it

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python inference.py

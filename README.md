---
title: Smart Email Triage Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Smart Email Triage Environment

An RL environment for training agents to intelligently triage emails — built following the OpenEnv framework by Meta & Hugging Face.

## What it does

An agent processes 25 diverse emails one by one and decides:
- `escalate` — urgent, needs immediate human attention
- `reply` — normal email needing a response
- `archive` — spam or irrelevant
- `flag` — security threat or phishing

## Reward Logic

| Situation | Reward |
|---|---|
| Correctly escalated urgent email | +2.0 |
| Correctly flagged security threat | +1.5 |
| Correctly replied or archived | +1.0 |
| Missed urgent email | -2.0 |
| Missed security threat | -1.5 |
| Unnecessary escalation | -1.0 |
| Other wrong decision | -0.5 |

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/reset` | POST | Start new episode, returns first email |
| `/step` | POST | Submit decision, returns next email + reward |
| `/history` | GET | Full decision log |
| `/grade` | GET | Score, accuracy, total reward |
| `/grade_llm` | GET | LLM-based semantic evaluation of agent |

## Running Locally
```bash
pip install -r requirements.txt
uvicorn inference:app --host 0.0.0.0 --port 7860
```

## Example Episode
```
Email: 'URGENT: Server Down' → escalate ✅ +2.0
Email: 'Win a FREE iPhone!' → archive ✅ +1.0
Email: 'Phishing attempt' → flag ✅ +1.5
Final Score: 8.5 | Accuracy: 100%
```
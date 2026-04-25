---
title: Smart Email Triage Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# Smart Email Triage Environment

An RL environment where an AI agent learns to triage emails by classifying them as `escalate`, `reply`, `archive`, or `flag`. Simulates real-world email management at scale.

## Why This Matters
Enterprise workers spend 28% of their workday on email. This environment trains agents to prioritize critical emails, reduce response time, and avoid costly mistakes like missing urgent security alerts.

## Environment Description
The agent receives emails one at a time and must classify each into one of 4 actions. Rewards are shaped to reflect real business consequences — missing an escalation is penalized more than misclassifying spam.

## Action Space
| Action | Description |
|--------|-------------|
| `escalate` | Urgent — requires immediate human attention |
| `reply` | Needs a response but not urgent |
| `archive` | Low priority, no action needed |
| `flag` | Suspicious — potential security threat |

## Observation Space
| Field | Type | Description |
|-------|------|-------------|
| `email_id` | int | Unique email identifier |
| `subject` | string | Email subject line |
| `sender` | string | Sender email address |
| `body` | string | Email body content |
| `task` | string | Current task difficulty |
| `difficulty` | string | easy / medium / hard / meeting |

## Tasks
| Task | Description | Baseline Score |
|------|-------------|----------------|
| `easy` | Obviously spam or urgent emails | 0.85 |
| `medium` | Emails requiring context awareness | 0.75 |
| `hard` | Ambiguous emails requiring expert judgment | 0.65 |
| `meeting` | Resolve meeting conflicts under pressure | 0.66 |

## Reward Function
Rewards reflect real business consequences:
- Correct classification: `0.95`
- Missing an escalation: `0.05` (high penalty)
- Flagging suspicious email correctly: `0.95`
- Wrong action on urgent email: `0.05`
- Partial credit for related actions: `0.15-0.30`

All rewards are strictly within `(0.01, 0.99)`.

Anti-reward-hacking checks are built in:
- Invalid actions are penalized with reward `0.01`
- Agents spamming the same action get reduced rewards
- Episode timeout after 5 minutes or 50 steps

## Training Evidence

### Training Loss & Reward Curves
![Training Curves](training_curves.png)
*Loss decreases and reward improves over 3 training epochs*

### Before vs After Training
![Before After](before_after.png)

| Task | Before Training | After Training | Improvement |
|------|----------------|----------------|-------------|
| easy | 0.45 | 0.85 | +0.40 |
| medium | 0.35 | 0.75 | +0.40 |
| hard | 0.25 | 0.65 | +0.40 |
| meeting | 0.20 | 0.66 | +0.46 |

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reset?task=easy` | POST | Start new episode |
| `/step` | POST | Take action |
| `/state` | GET | Get current state |
| `/grade` | GET | Get episode score |
| `/history` | GET | Get full history |

## Quick Start
```python
import requests

ENV_URL = "https://shivanibalajii-smart-email-triage-env-final.hf.space"

# Start episode
obs = requests.post(f"{ENV_URL}/reset?task=easy").json()
print("Email:", obs["subject"])

# Take action
result = requests.post(f"{ENV_URL}/step", json={"action": "escalate"}).json()
print("Reward:", result["reward"]["reward"])
print("Correct:", result["reward"]["correct"])
```

## Setup & Usage

### Run locally
```bash
git clone https://github.com/shivanibalajii/smart-email-triage-env
cd smart-email-triage-env
pip install -r requirements.txt
uvicorn inference:app --host 0.0.0.0 --port 7860
```

### Run with Docker
```bash
docker build -t smart-email-triage .
docker run -p 7860:7860 smart-email-triage
```

### Run baseline agent
```bash
export API_BASE_URL=https://api-inference.huggingface.co/v1/
export API_KEY=your_hf_token
python inference.py
```

## Environment Variables
| Variable | Description |
|----------|-------------|
| `API_BASE_URL` | LLM API endpoint |
| `API_KEY` | API key |
| `MODEL_NAME` | Model to use (default: meta-llama/Llama-3.3-70B-Instruct) |
| `HF_TOKEN` | Hugging Face token |

## Resources
- 🤗 HF Space: https://huggingface.co/spaces/shivanibalajii/smart-email-triage-env-final
- 💻 GitHub: https://github.com/shivanibalajii/smart-email-triage-env
- 📓 Training Notebook: https://colab.research.google.com/drive/1RhSbTh7xexLx9pAzlvAknuIPNUKnvI_6?usp=sharing
- 📝 Blog: https://huggingface.co/shivanibalajii/smart-email-triage-blog

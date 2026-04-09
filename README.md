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
| `difficulty` | string | easy / medium / hard |

## Tasks
| Task | Description | Baseline Score |
|------|-------------|----------------|
| `easy` | Obviously spam or urgent emails | 0.85 |
| `medium` | Emails requiring context awareness | 0.75 |
| `hard` | Ambiguous emails needing nuanced judgment | 0.65 |

## Reward Function
Rewards reflect real business consequences:
- Correct classification: `0.95`
- Missing an escalation: `0.05` (high penalty)
- Flagging suspicious email correctly: `0.95`
- Wrong action on urgent email: `0.05`
- Partial credit for related actions: `0.15-0.30`

All rewards are strictly within `(0.01, 0.99)`.

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/reset?task=easy` | POST | Start new episode |
| `/step` | POST | Take action |
| `/state` | GET | Get current state |
| `/grade` | GET | Get episode score |
| `/history` | GET | Get full history |

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

## Baseline Scores
| Task | Score |
|------|-------|
| easy | 0.85 |
| medium | 0.75 |
| hard | 0.65 |

## Environment Variables
| Variable | Description |
|----------|-------------|
| `API_BASE_URL` | LLM API endpoint |
| `API_KEY` | API key |
| `MODEL_NAME` | Model to use (default: meta-llama/Llama-3.3-70B-Instruct) |
| `HF_TOKEN` | Hugging Face token |

## HF Space
https://huggingface.co/spaces/shivanibalajii/smart-email-triage-env-final
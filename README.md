# Smart Email Triage Environment

An RL environment for training agents to intelligently triage emails — built on the OpenEnv framework by Meta & Hugging Face.

## What it does

An agent processes a batch of emails one by one and must decide what to do with each:
- `escalate` — urgent, needs immediate human attention
- `reply` — normal email needing a response  
- `archive` — spam or irrelevant

The environment rewards correct decisions and penalises wrong ones, with extra weight on critical emails.

## Reward Logic

| Situation | Reward |
|---|---|
| Correctly escalated urgent email | +2.0 |
| Correctly replied to normal email | +1.0 |
| Correctly archived spam | +1.0 |
| Missed an urgent email (should have escalated) | -2.0 |
| Unnecessary escalation | -1.0 |
| Other wrong decision | -0.5 |

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/reset` | POST | Start a new episode, returns first email |
| `/step` | POST | Submit a decision, returns next email + reward |
| `/history` | GET | Full decision log for current episode |
| `/grade` | GET | Final score, accuracy, total reward |

## Running Locally
```bash
pip install -r requirements.txt
uvicorn inference:app --host 0.0.0.0 --port 7860
```

Then run the client agent:
```bash
python client.py
```

## Example Episode
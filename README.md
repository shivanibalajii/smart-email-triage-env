#  Smart Email Triage Environment (OpenEnv RL)

##  What this project is

This project simulates a real-world email inbox where an agent has to decide how to handle incoming emails.

Instead of just storing or displaying emails, this is built as a **reinforcement learning environment** using the OpenEnv framework.
The agent interacts with the system step-by-step and learns to make better decisions over time.

---

## What the environment does

The environment presents emails one at a time.
Each email has a hidden “correct action” (like escalate or archive), and the agent must choose how to handle it.

The goal is simple:
 prioritize important emails correctly
 avoid wasting time on spam or low-priority messages

---

## 🎯 Available Actions

The agent can choose one of the following actions for each email:

* `reply` → respond to normal emails
* `escalate` → mark urgent emails for immediate attention
* `archive` → ignore spam or irrelevant emails
* `flag` → mark suspicious emails

---

##  Reward Function

The environment gives feedback based on the agent’s decision:

* +1 → correct decision
* -1 → incorrect decision

This encourages the agent to learn proper prioritization.

---

##  Example Episode

Step 1
Email: URGENT: Server Down
Agent Action: escalate
Reward: +1

Step 2
Email: Win a FREE iPhone!!!
Agent Action: reply
Reward: -1

Step 3
Email: Meeting Reminder
Agent Action: reply
Reward: +1

---

## Environment Design

This project follows the OpenEnv structure:

* `reset()` → starts a new episode and returns the first email
* `step(action)` → processes the agent’s decision and returns:

  * next email
  * reward
  * done (whether episode is finished)

The environment is implemented using a Gym-style interaction loop.

---

##  Project Structure

```
.
├── server/
│   ├── email_environment.py
│
├── models.py
├── inference.py
├── client.py
├── grader.py
├── openenv.yaml
```

---

##  How to Run

### 1. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the server

```bash
uvicorn inference:app --reload
```

---

##  API Endpoints

### POST `/reset`

Starts a new episode
Returns the first email observation

---

### POST `/step`

Takes an action and returns:

* next email
* reward
* done

Example input:

```json
{
  "email_id": "1",
  "decision": "escalate"
}
```

---

## Client Simulation

A simple client (`client.py`) is included to simulate interaction with the environment step-by-step.

---

## Grading Logic

The grader evaluates how well the agent performs across an episode by checking correct vs incorrect decisions.

---

## Why this matters

Email overload is a real problem.
This environment models a practical scenario where AI can help prioritize communication efficiently.

---

##  Summary

This project transforms a basic email system into an interactive RL environment where:

* decisions matter
* feedback is immediate
* learning is possible

---

##  Author

Shivani

import requests

BASE_URL = "http://localhost:7860"

def run_episode():
    obs = requests.post(f"{BASE_URL}/reset").json()
    print(f"Starting episode...\nFirst email: {obs['email_subject']}\n")

    done = False
    while not done:
        subject = obs.get("email_subject", "").upper()
        sender = obs.get("email_sender", "")

        # Simple rule-based agent
        if "URGENT" in subject or "boss" in sender or "manager" in sender:
            decision = "escalate"
        elif "FREE" in subject or "spam" in sender or "WIN" in subject:
            decision = "archive"
        else:
            decision = "reply"

        action = {"email_id": obs["email_id"], "decision": decision}
        print(f"Email: '{obs['email_subject']}' → Decision: {decision}")

        obs = requests.post(f"{BASE_URL}/step", json=action).json()
        done = obs["done"]

    result = requests.get(f"{BASE_URL}/grade").json()
    print(f"\nEpisode complete!")
    print(f"Score: {result['total_reward']} | Accuracy: {result['accuracy']*100:.0f}%")

if __name__ == "__main__":
    run_episode()
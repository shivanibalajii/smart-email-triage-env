from app.env import EmailEnv
from app.models import Action
import random

print("[START]")

env = EmailEnv()
obs = env.reset()

rewards = []

for i, email in enumerate(obs.emails):

    print(f"\nProcessing Email {i+1}")
    print("Subject:", email.subject)
    print("Sender:", email.sender)

    # small randomness to simulate imperfect agent
    if random.random() < 0.05:
        action = Action(action_type="reply", email_index=i)
    else:
        if email.sender == "boss":
            action = Action(action_type="escalate", email_index=i)
        elif email.sender == "spam":
            action = Action(action_type="ignore", email_index=i)
        else:
            action = Action(action_type="reply", email_index=i)

    print("Action Taken:", action.action_type)

    result = env.step(action)

    print("Reward:", result.reward)

    rewards.append(result.reward)

print("\n[END]")
print("Final Score:", sum(rewards))
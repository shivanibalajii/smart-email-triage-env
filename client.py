from openenv.core.env_client import EnvClient
from models import EmailAction

client = EnvClient(base_url="http://localhost:8000")

obs = client.reset()

done = False

while not done:
    print("Email:", obs.email_subject)

    action = EmailAction(
        email_id=obs.email_id,
        decision="reply"  # dummy decision
    )

    obs = client.step(action)
    done = obs.done
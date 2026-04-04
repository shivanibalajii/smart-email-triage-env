from openenv_core.environment import Environment
from models import EmailAction, EmailObservation
import random

class EmailEnvironment(Environment):

    def __init__(self):
        self.emails = []
        self.current_index = 0

    def reset(self):
        self.emails = [
            {
                "id": "1",
                "subject": "URGENT: Server Down",
                "sender": "boss@company.com",
                "body": "Fix immediately",
                "label": "escalate"
            },
            {
                "id": "2",
                "subject": "Meeting Reminder",
                "sender": "hr@company.com",
                "body": "Team meeting at 3 PM",
                "label": "reply"
            },
            {
                "id": "3",
                "subject": "Win a FREE iPhone!!!",
                "sender": "spam@fake.com",
                "body": "Click now",
                "label": "archive"
            }
        ]
        self.current_index = 0

        email = self.emails[self.current_index]

        return EmailObservation(
            email_id=email["id"],
            email_subject=email["subject"],
            email_sender=email["sender"],
            email_body=email["body"],
            reward=0.0,
            done=False
        )

    def step(self, action: EmailAction):
        email = self.emails[self.current_index]

        correct_action = email["label"]

        # reward logic
        if action.decision == correct_action:
            reward = 1.0
        else:
            reward = -1.0

        self.current_index += 1
        done = self.current_index >= len(self.emails)

        if not done:
            next_email = self.emails[self.current_index]
            return EmailObservation(
                email_id=next_email["id"],
                email_subject=next_email["subject"],
                email_sender=next_email["sender"],
                email_body=next_email["body"],
                reward=reward,
                done=False
            )
        else:
            return EmailObservation(
                email_id="",
                email_subject="",
                email_sender="",
                email_body="",
                reward=reward,
                done=True
            )
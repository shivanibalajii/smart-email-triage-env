from models import EmailAction, EmailObservation

EMAILS = [
    {"id": "1", "subject": "URGENT: Server Down", "sender": "boss@company.com",
     "body": "Production is down, fix immediately!", "label": "escalate"},
    {"id": "2", "subject": "Meeting Reminder", "sender": "hr@company.com",
     "body": "Team meeting at 3 PM today.", "label": "reply"},
    {"id": "3", "subject": "Win a FREE iPhone!!!", "sender": "spam@fake.com",
     "body": "Click now to claim your prize.", "label": "archive"},
    {"id": "4", "subject": "URGENT: Client Complaint", "sender": "manager@company.com",
     "body": "Major client is unhappy, needs immediate response.", "label": "escalate"},
    {"id": "5", "subject": "Newsletter: Weekly Digest", "sender": "news@medium.com",
     "body": "Your weekly reading list is here.", "label": "archive"},
    {"id": "6", "subject": "Quick question about the report", "sender": "colleague@company.com",
     "body": "Can you clarify section 3?", "label": "reply"},
]

class EmailEnvironment:
    def __init__(self):
        self.emails = []
        self.current_index = 0
        self.history = []

    def reset(self):
        self.emails = EMAILS.copy()
        self.current_index = 0
        self.history = []
        email = self.emails[0]
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
        correct = email["label"]

        # Nuanced reward logic
        if action.decision == correct:
            # Bigger reward for correctly handling critical emails
            reward = 2.0 if correct == "escalate" else 1.0
        elif correct == "escalate" and action.decision != "escalate":
            reward = -2.0  # Missing urgent email is worst mistake
        elif correct != "escalate" and action.decision == "escalate":
            reward = -1.0  # Unnecessary escalation is bad
        else:
            reward = -0.5  # Wrong but not catastrophic

        self.history.append({
            "email_id": email["id"],
            "correct_action": correct,
            "agent_action": action.decision,
            "reward": reward,
            "correct": action.decision == correct
        })

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
                email_id="done",
                email_subject="Episode complete",
                email_sender="",
                email_body="",
                reward=reward,
                done=True
            )

    def get_history(self):
        return self.history
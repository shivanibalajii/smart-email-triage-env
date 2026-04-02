from app.models import Email, Observation, Action, StepResult
import random


class EmailEnv:

    def __init__(self):
        self.emails = []
        self.current = 0
        self.step_count = 0

    def reset(self):
        # Realistic + random emails
        possible_emails = [
            Email(
                subject="URGENT: Production Server Down",
                body="Critical outage affecting all users. Immediate action required.",
                sender="boss",
                priority=3
            ),
            Email(
                subject="Team Meeting Reminder",
                body="Reminder: Meeting scheduled tomorrow at 10 AM.",
                sender="team",
                priority=2
            ),
            Email(
                subject="Limited Time Offer!!!",
                body="Get 70% discount on products. Buy now!!!",
                sender="spam",
                priority=1
            ),
            Email(
                subject="Client Escalation Issue",
                body="Client is unhappy with the service. Needs urgent response.",
                sender="boss",
                priority=3
            ),
            Email(
                subject="Weekly Report Submission",
                body="Please submit your weekly report by EOD.",
                sender="team",
                priority=2
            ),
            Email(
                subject="Win a Free iPhone!!!",
                body="Click here to claim your reward.",
                sender="spam",
                priority=1
            )
        ]

        self.emails = random.sample(possible_emails, k=3)

        self.current = 0
        self.step_count = 0

        return Observation(emails=self.emails, step_count=0)

    def state(self):
        return {
            "current_email_index": self.current,
            "step_count": self.step_count
        }

    def step(self, action: Action):

        email = self.emails[action.email_index]

        reward = 0

        # Reward design prioritizes critical decision-making:
        # high-importance emails (boss) have higher penalties for mistakes
        if email.sender == "boss":
            if action.action_type == "escalate":
                reward = 1.0
            else:
                reward = -1.0

        elif email.sender == "team":
            if action.action_type == "reply":
                reward = 0.8
            else:
                reward = -0.3

        elif email.sender == "spam":
            if action.action_type == "ignore":
                reward = 0.5
            else:
                reward = -0.2

        self.step_count += 1
        self.current += 1

        done = self.current >= len(self.emails)

        return StepResult(
            observation=Observation(
                emails=self.emails,
                step_count=self.step_count
            ),
            reward=reward,
            done=done,
            info={}
        )
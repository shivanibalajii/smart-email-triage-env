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
    {"id": "7", "subject": "SECURITY ALERT: Suspicious login detected", "sender": "security@company.com",
     "body": "A login was detected from an unknown device in Russia.", "label": "flag"},
    {"id": "8", "subject": "Your invoice is overdue", "sender": "billing@vendor.com",
     "body": "Payment of $5000 is overdue by 30 days.", "label": "escalate"},
    {"id": "9", "subject": "Claim your lottery winnings!", "sender": "lottery@scam.com",
     "body": "You have won $1,000,000. Send your bank details.", "label": "archive"},
    {"id": "10", "subject": "Follow up on project deadline", "sender": "teammate@company.com",
     "body": "Just checking in on the deliverable due Friday.", "label": "reply"},
    {"id": "11", "subject": "URGENT: Data breach detected", "sender": "cto@company.com",
     "body": "Customer data may be compromised. All hands on deck.", "label": "escalate"},
    {"id": "12", "subject": "Phishing attempt: verify your account", "sender": "support@fake-bank.com",
     "body": "Click here to verify your bank account immediately.", "label": "flag"},
    {"id": "13", "subject": "Team lunch this Friday", "sender": "hr@company.com",
     "body": "We are doing a team lunch at 1 PM, please RSVP.", "label": "reply"},
    {"id": "14", "subject": "Congratulations! You are selected", "sender": "noreply@scam.net",
     "body": "You have been selected for a cash prize. Act now!", "label": "archive"},
    {"id": "15", "subject": "URGENT: Legal notice received", "sender": "legal@company.com",
     "body": "We have received a legal notice that requires immediate attention.", "label": "escalate"},
    {"id": "16", "subject": "Suspicious attachment from unknown sender", "sender": "unknown123@gmail.com",
     "body": "Please open the attached file for important information.", "label": "flag"},
    {"id": "17", "subject": "Performance review scheduled", "sender": "manager@company.com",
     "body": "Your annual performance review is scheduled for next Monday.", "label": "reply"},
    {"id": "18", "subject": "FREE vacation package just for you", "sender": "deals@spammer.com",
     "body": "Claim your free vacation package today, limited slots!", "label": "archive"},
    {"id": "19", "subject": "URGENT: CEO request for wire transfer", "sender": "ceo-fake@gmail.com",
     "body": "Transfer $50,000 immediately to this account, very urgent.", "label": "flag"},
    {"id": "20", "subject": "System maintenance tonight", "sender": "it@company.com",
     "body": "Planned downtime from 2 AM to 4 AM for system updates.", "label": "reply"},
    {"id": "21", "subject": "URGENT: Customer threatening lawsuit", "sender": "support@company.com",
     "body": "A customer is threatening legal action over a defective product.", "label": "escalate"},
    {"id": "22", "subject": "Your password was changed", "sender": "noreply@suspicioussite.com",
     "body": "Your password was recently changed. If not you, click here.", "label": "flag"},
    {"id": "23", "subject": "Feedback on last weeks presentation", "sender": "director@company.com",
     "body": "Great work on the presentation, a few suggestions attached.", "label": "reply"},
    {"id": "24", "subject": "Make money fast working from home", "sender": "jobs@scamjobs.com",
     "body": "Earn $5000 a week from home, no experience needed.", "label": "archive"},
    {"id": "25", "subject": "URGENT: Server costs exceeding budget", "sender": "finance@company.com",
     "body": "AWS costs have tripled this month, immediate review needed.", "label": "escalate"},
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

        if action.decision == correct:
            if correct == "escalate":
                reward = 2.0
            elif correct == "flag":
                reward = 1.5
            else:
                reward = 1.0
        elif correct == "escalate" and action.decision != "escalate":
            reward = -2.0  # Missing urgent email is worst
        elif correct == "flag" and action.decision == "archive":
            reward = -1.5  # Missing security threat is very bad
        elif correct != "escalate" and action.decision == "escalate":
            reward = -1.0  # Unnecessary escalation
        else:
            reward = -0.5  # Wrong but not catastrophic

        self.history.append({
            "email_id": email["id"],
            "email_subject": email["subject"],
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
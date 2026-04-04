from pydantic import BaseModel

class EmailAction(BaseModel):
    email_id: str
    decision: str  # "reply", "escalate", "archive", "flag"

class EmailObservation(BaseModel):
    email_id: str
    email_subject: str
    email_sender: str
    email_body: str
    reward: float
    done: bool
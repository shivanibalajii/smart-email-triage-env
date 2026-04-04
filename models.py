from openenv_core.models import Action, Observation
from pydantic import BaseModel

class EmailAction(Action):
    email_id: str
    decision: str  # "reply", "escalate", "archive", "flag"

class EmailObservation(Observation):
    email_id: str
    email_subject: str
    email_sender: str
    email_body: str
    reward: float
    done: bool
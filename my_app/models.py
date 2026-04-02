from pydantic import BaseModel
from typing import List

class Email(BaseModel):
    subject: str
    body: str
    sender: str
    priority: int

class Observation(BaseModel):
    emails: List[Email]
    step_count: int

class Action(BaseModel):
    action_type: str
    email_index: int

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict
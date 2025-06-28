from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    sender: str
    duration: float
    text: str

class Conversation(BaseModel):
    messages: List[Message]
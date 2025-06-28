"""
models/conversation.py

Defines data models for representing a conversation and its individual messages.
"""

from pydantic import BaseModel
from typing import List

class Message(BaseModel):
    """
    Represents a single message in a conversation.

    Attributes:
        sender (str): The origin of the message (e.g., "user" or "robot").
        duration (float): The estimated duration of the message in seconds.
        text (str): The transcribed content of the message.
    """
    sender: str
    duration: float
    text: str

class Conversation(BaseModel):
    """
    Represents a full conversation as a sequence of messages.

    Attributes:
        messages (List[Message]): A list of individual messages that form the conversation.
    """
    messages: List[Message]

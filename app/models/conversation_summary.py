"""
models/conversation_summary.py

Defines data models for representing conversation summaries.
"""

from pydantic import BaseModel
from typing import List

class ConversationSummary(BaseModel):
    """
    Represents a summarized conversation with key information.

    Attributes:
        title (str): The title or subject of the conversation.
        summary (str): A comprehensive summary of the conversation.
        user_demands_points (List[str]): List of specific points or demands
                                         raised by the user during the conversation.
    """
    title: str
    summary: str
    user_demands_points: List[str]

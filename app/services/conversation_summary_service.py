"""
Conversation Summary Service

This module provides services for generating structured summaries of conversations using OpenAI.
"""

from typing import List
import json
from app.models.conversation_summary import ConversationSummary
from app.utils.prompt_templates import generate_conversation_summary_prompt
from app.core.config import settings
import openai

openai.api_key = settings.openai_api_key

class ConversationSummaryService:
    """
    Service for generating structured conversation summaries using OpenAI.
    """

    def __init__(self):
        """
        Initialize the conversation summary service.
        """
        pass

    def generate_summary(self, conversation_text: str) -> ConversationSummary:
        """
        Generate a structured summary of a conversation using OpenAI.

        Args:
            conversation_text (str): The full text of the conversation.

        Returns:
            ConversationSummary: A structured summary of the conversation.

        Raises:
            ValueError: If the OpenAI response cannot be parsed or is missing required fields.
        """
        prompt = generate_conversation_summary_prompt(conversation_text)
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in conversation analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
            )
            
            content = response.choices[0].message.content.strip()
            
            summary_data = json.loads(content)
            
            return ConversationSummary(
                title=summary_data["title"],
                summary=summary_data["summary"],
                user_demands_points=summary_data["user_demands_points"]
            )
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse OpenAI response: {str(e)}")
        except KeyError as e:
            raise ValueError(f"Missing required field in response: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to generate summary: {str(e)}")

    def get_conversation_points(self, conversation_text: str) -> List[str]:
        """
        Extract just the user demands points from a conversation using OpenAI.

        Args:
            conversation_text (str): The full text of the conversation.

        Returns:
            List[str]: List of user demands/points raised in the conversation.
        """
        summary = self.generate_summary(conversation_text)
        return summary.user_demands_points

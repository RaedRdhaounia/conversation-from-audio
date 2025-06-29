"""
routes/transcription.py

This module provides an endpoint to process an audio URL and return
a transcribed conversation with speaker labels, wrapped in a standardized response format.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from urllib.parse import urlparse
from app.models.response import ResponseWrapper
from app.models.conversation import Conversation
from app.services.transcriber import process_audio_url
from app.core.config import settings
import time

transcription_router = APIRouter(prefix="/api", tags=["Transcription"])

class TranscriptionRequest(BaseModel):
    """
    Request model for audio transcription.

    Attributes:
        audio_url (str): A valid HTTP or HTTPS URL pointing to an audio file.
    """

    audio_url: str

    @validator("audio_url")
    def validate_url(cls, v: str) -> str:
        """
        Validates that the audio_url is a properly formatted HTTP or HTTPS URL.

        Args:
            v (str): The URL provided in the request.

        Returns:
            str: The same URL if it's valid.

        Raises:
            ValueError: If the URL is invalid.
        """
        parsed = urlparse(v)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Invalid URL. Please provide a valid HTTP or HTTPS link.")
        return v


@transcription_router.post(
    "/conversation",
    response_model=ResponseWrapper,
    summary="Transcribe an audio URL",
    response_description="A standardized response containing the transcription result."
)
async def get_conversation(request: TranscriptionRequest):
    """
    Processes the provided audio URL and returns a transcribed conversation.

    Args:
        request (TranscriptionRequest): The request body containing the audio_url.

    Returns:
        ResponseWrapper: A standardized response including status, success flag, message, and transcription data.

    Raises:
        HTTPException: Returns status 500 if an error occurs during processing.
    """
    try:
        conversation: Conversation = await process_audio_url(request.audio_url)
        return ResponseWrapper(
            status=200,
            success=True,
            message="Transcription completed successfully.",
            data=conversation.dict(),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ResponseWrapper(
                status=500,
                success=False,
                message=f"An error occurred during transcription: {str(e)}",
                data=None,
            ).dict()
        )


@transcription_router.patch(
    "conversation",
    summary="Deep Health Check (Transcriber Test)",
    response_description="Verifies audio processing pipeline works correctly.",
    response_model=ResponseWrapper
)
async def test_transcriber_pipeline(request: Request):
    """
    Performs a deeper health check by running the transcription pipeline
    against a known test audio file from the environment.

    Returns:
        ResponseWrapper: Includes details of the transcribed messages and performance metrics.
    """
    try:
        start_time = time.time()

        audio_url_str = str(settings.test_audio_url)
        conversation: Conversation = await process_audio_url(audio_url_str)

        end_time = time.time()
        duration_ms = round((end_time - start_time) * 1000, 2)

        message_count = len(conversation.messages)
        total_text_length = sum(len(msg.text or "") for msg in conversation.messages)
        input_url_size_bytes = len(audio_url_str.encode("utf-8"))

        return ResponseWrapper(
            status=200,
            success=True,
            message="Transcriber pipeline succeeded.",
            data={
                "messages": [msg.dict() for msg in conversation.messages],
                "performance": {
                    "duration_ms": duration_ms,
                    "message_count": message_count,
                    "total_text_length": total_text_length,
                    "input_url_size_bytes": input_url_size_bytes
                }
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=ResponseWrapper(
                status=500,
                success=False,
                message="Transcriber pipeline failed.",
                data={"error": str(e)}
            ).dict()
        )

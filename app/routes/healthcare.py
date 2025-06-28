"""
app/routes/healthcare.py

Defines the /healthcare endpoint used as a basic health check
for the Voice Transcriber Service.
"""

from fastapi import APIRouter, HTTPException, Request
from app.models.response import ResponseWrapper
from app.core.config import settings
from app.services.transcriber import process_audio_url
from app.models.conversation import Conversation
import time

healthcare_router = APIRouter(
    prefix="/healthcare",
    tags=["Health"]
)

@healthcare_router.get(
    "",
    summary="Health Check",
    response_description="A confirmation that the service is operational.",
    response_model=ResponseWrapper
)
async def healthcare_status():
    """
    Returns a basic health check status to indicate the system is up.

    This endpoint can be used by monitoring tools or deployment platforms
    to verify that the service is running.

    Returns:
        ResponseWrapper: Standardized API response indicating the system is healthy.
    """
    return ResponseWrapper(
        status=200,
        success=True,
        message="Healthcare system is up.",
        data={"status": "ok"},
    )

@healthcare_router.patch(
    "",
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

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

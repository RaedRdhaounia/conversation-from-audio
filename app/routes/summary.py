from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.services.conversation_summary_service import ConversationSummaryService
from app.services.transcriber import process_audio_url
from app.models.conversation_summary import ConversationSummary
from app.models.response import ResponseWrapper
from app.core.config import settings
import time

summary_router = APIRouter(prefix="/api", tags=["Summary"])

class AudioSummaryRequest(BaseModel):
    audio_url: str

@summary_router.post("/summarize-audio", response_model=ResponseWrapper)
async def summarize_audio(request: AudioSummaryRequest):
    """
    Generate a summary of an audio conversation.

    Args:
        request (AudioSummaryRequest): Request containing the audio URL.

    Returns:
        ResponseWrapper: Standardized response containing the conversation summary.

    Raises:
        HTTPException: If audio processing fails or summary generation fails.
    """
    try:
        conversation = await process_audio_url(request.audio_url)
        transcript = " ".join([msg.text for msg in conversation.messages])
        summary_service = ConversationSummaryService()
        summary = summary_service.generate_summary(transcript)
        
        return ResponseWrapper(
            status=200,
            success=True,
            message="Conversation summary generated successfully.",
            data={
                "title": summary.title,
                "summary": summary.summary,
                "user_demands_points": summary.user_demands_points
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ResponseWrapper(
                status=500,
                success=False,
                message=f"Failed to process audio and generate summary: {str(e)}",
                data=None,
            ).dict()
        )

@summary_router.patch(
    "/summarize-audio",
    summary="Deep Health Check (Summary Test)",
    response_description="Verifies summary pipeline works correctly.",
    response_model=ResponseWrapper
)
async def test_summary_pipeline(request: Request):
    """
    Performs a deeper health check by running the summary pipeline
    against a known test audio file from the environment.

    Returns:
        ResponseWrapper: Includes details of the summary generation and performance metrics.
    """
    try:
        start_time = time.time()

        audio_url_str = str(settings.test_audio_url)
        conversation = await process_audio_url(audio_url_str)
        
        transcript = " ".join([msg.text for msg in conversation.messages])
        
        summary_service = ConversationSummaryService()
        
        summary = summary_service.generate_summary(transcript)

        end_time = time.time()
        duration_ms = round((end_time - start_time) * 1000, 2)

        message_count = len(conversation.messages)
        total_text_length = sum(len(msg.text or "") for msg in conversation.messages)
        input_url_size_bytes = len(audio_url_str.encode("utf-8"))

        return ResponseWrapper(
            status=200,
            success=True,
            message="Summary pipeline succeeded.",
            data={
                "summary": {
                    "title": summary.title,
                    "summary": summary.summary,
                    "user_demands_points": summary.user_demands_points
                },
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
                message="Summary pipeline failed.",
                data={"error": str(e)}
            ).dict()
        )

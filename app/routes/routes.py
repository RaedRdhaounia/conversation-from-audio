from fastapi import APIRouter, Query, HTTPException
from app.services.transcriber import process_audio_url
from app.models.conversation import Conversation

router = APIRouter(prefix="/api")

@router.get("/conversation", response_model=Conversation)
async def get_conversation(
    audio_url: str = Query(..., description="Public URL of MP3/WAV file"),
    duration: float = Query(..., description="Total call duration in seconds"),
):
    try:
        return await process_audio_url(audio_url, duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

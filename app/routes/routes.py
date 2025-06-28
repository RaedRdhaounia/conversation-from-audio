from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.transcriber import process_audio_url
from app.models.conversation import Conversation

router = APIRouter(prefix="/api")

class TranscriptionRequest(BaseModel):
    audio_url: str

@router.post("/conversation", response_model=Conversation)
async def get_conversation(request: TranscriptionRequest):
    try:
        return await process_audio_url(request.audio_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

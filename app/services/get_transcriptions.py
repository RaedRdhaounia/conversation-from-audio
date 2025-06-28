from app.core.config import settings
import openai

openai.api_key = settings.openai_api_key

def transcribe_with_whisper(audio_path: str) -> str:
    """
    Transcribes audio from a given file path using OpenAI's Whisper API.

    Args:
        audio_path (str): Path to the audio file to transcribe.

    Returns:
        str: The transcribed text from the audio.

    Raises:
        openai.error.OpenAIError: If the transcription request fails.
    """
    resp = openai.audio.transcriptions.create(
        file=open(audio_path, "rb"),
        model="whisper-1",
        response_format="text",
    )
    return resp

import aiohttp, asyncio, tempfile, os, json
from typing import List
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import librosa
import openai
from app.core.config import settings
from app.models.conversation import Message, Conversation

encoder = VoiceEncoder()
openai.api_key = settings.openai_api_key

# ---------- helper --------------------------------------------------------- #
async def _download_file(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.read()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(data)
    tmp.close()
    return tmp.name

def _load_or_create_robot_embed(robot_profile_path: str, wav_path: str) -> np.ndarray:
    if os.path.exists(robot_profile_path):
        return np.load(robot_profile_path)
    wav, _ = librosa.load(wav_path, sr=None)
    embed = encoder.embed_utterance(wav)
    os.makedirs(os.path.dirname(robot_profile_path), exist_ok=True)
    np.save(robot_profile_path, embed)
    return embed

# --------------------------------------------------------------------------- #
async def transcribe_with_whisper(audio_path: str) -> str:
    resp = openai.audio.transcriptions.create(
        file=open(audio_path, "rb"),
        model="whisper-1",
        response_format="text",
    )
    return resp

def split_to_sentences(text: str) -> List[str]:
    import re
    return re.split(r"(?<=[.!?])\s+", text.strip())

def estimate_durations(n_sentences: int, total_seconds: float) -> List[float]:
    per = total_seconds / max(n_sentences, 1)
    return [per] * n_sentences

def speaker_label_segments(sentences: List[str], robot_embed: np.ndarray) -> List[str]:
    """
    Very lightweight heuristic:
    - extract embedding from each sentence audio slice (NOT implemented here)
    - compare cosine similarity with robot_embed
    - if similarity > thresh: robot else user
    Placeholder returns alternation for now.
    """
    labels = []
    for i, _ in enumerate(sentences):
        labels.append("robot" if i % 2 == 0 else "user")
    return labels

# ---------------- public service fn --------------------------------------- #
async def process_audio_url(audio_url: str, total_duration: float) -> Conversation:
    local_path = await _download_file(audio_url)

    # ---- transcription text ----
    transcript = await asyncio.to_thread(transcribe_with_whisper, local_path)

    # ---- sentence splitting + duration estimation ----
    sentences = split_to_sentences(transcript)
    durations = estimate_durations(len(sentences), total_duration)

    # ---- speaker labelling (placeholder alternation) ----
    # In production replace with real embedding comparison
    robot_embed = np.zeros(256)  # placeholder
    try:
        robot_embed = _load_or_create_robot_embed(settings.robot_profile_path, local_path)
    except Exception:
        pass
    labels = speaker_label_segments(sentences, robot_embed)

    messages = [
        Message(sender=labels[i], duration=durations[i], text=sentences[i])
        for i in range(len(sentences))
        if sentences[i]
    ]

    os.remove(local_path)
    return Conversation(messages=messages)

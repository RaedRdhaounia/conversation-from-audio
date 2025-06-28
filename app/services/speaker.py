import tempfile
from fastapi import UploadFile
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

encoder = VoiceEncoder()

async def process_audio_file(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    wav = preprocess_wav(tmp_path)
    embed = encoder.embed_utterance(wav)

    return {
        "embedding_shape": embed.shape,
        "summary": "Embedding extracted. Use this for speaker comparison.",
    }

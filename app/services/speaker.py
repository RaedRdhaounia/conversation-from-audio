import aiofiles
import os
import tempfile
import uuid
from fastapi import UploadFile
from resemblyzer import VoiceEncoder, preprocess_wav

encoder = VoiceEncoder()

async def process_audio_file(file: UploadFile):
    """
    /**
     * Processes an uploaded audio file asynchronously to extract a speaker embedding.
     *
     * @param {UploadFile} file - The uploaded audio file (expected .wav).
     * @returns {dict} - Dictionary containing embedding shape and a summary message.
     *
     * @remarks
     * Generates a unique temporary filename asynchronously without blocking.
     * Writes the file asynchronously with aiofiles.
     */
    """
    temp_dir = tempfile.gettempdir()
    unique_filename = f"{uuid.uuid4()}.wav"
    tmp_path = os.path.join(temp_dir, unique_filename)

    async with aiofiles.open(tmp_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    wav = preprocess_wav(tmp_path)
    embed = encoder.embed_utterance(wav)

    os.remove(tmp_path)

    return {
        "embedding_shape": embed.shape,
        "summary": "Embedding extracted. Use this for speaker comparison.",
    }

import librosa
from typing import List

def get_audio_duration(path: str) -> float:
    y, sr = librosa.load(path, sr=None)
    return librosa.get_duration(y=y, sr=sr)

def estimate_durations(sentences: List[str], total_seconds: float) -> List[float]:
    word_counts = [len(s.split()) for s in sentences]
    total_words = sum(word_counts)
    return [(wc / total_words) * total_seconds for wc in word_counts]
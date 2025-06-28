import librosa
from typing import List

def get_audio_duration(path: str) -> float:
    """
    Calculate the duration of an audio file in seconds.

    Args:
        path (str): The local file path to the audio file.

    Returns:
        float: Duration of the audio file in seconds.

    Raises:
        FileNotFoundError: If the audio file does not exist at the given path.
        librosa.util.exceptions.ParameterError: If the audio cannot be loaded properly.
    """
    y, sr = librosa.load(path, sr=None)
    return librosa.get_duration(y=y, sr=sr)


def estimate_durations(sentences: List[str], total_seconds: float) -> List[float]:
    """
    Estimate the duration of each sentence proportional to its word count,
    given the total audio duration.

    Args:
        sentences (List[str]): List of sentences from the transcript.
        total_seconds (float): Total duration of the audio in seconds.

    Returns:
        List[float]: Estimated durations (in seconds) for each sentence,
                     proportional to its length relative to the entire transcript.

    Example:
        sentences = ["Hello world.", "How are you?"]
        total_seconds = 10
        # Returns a list of durations [5.0, 5.0]

    Notes:
        - Sentences with more words get a longer duration estimate.
        - The sum of all returned durations equals total_seconds.
    """
    word_counts = [len(s.split()) for s in sentences]
    total_words = sum(word_counts)
    return [(wc / total_words) * total_seconds for wc in word_counts]

import re
from typing import List

def split_to_sentences(text: str) -> List[str]:
    """
    Splits a given text into sentences based on punctuation delimiters.

    Args:
        text (str): The input text to be split.

    Returns:
        List[str]: A list of sentence strings extracted from the input text.

    Details:
        - Sentences are split at punctuation marks '.', '!', or '?' followed by whitespace.
        - Leading and trailing whitespace from the input text is removed before splitting.
    """
    return re.split(r"(?<=[.!?])\s+", text.strip())

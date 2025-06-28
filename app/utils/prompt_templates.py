from typing import List

def generate_speaker_labeling_prompt(sentences: List[str]) -> str:
    """
    Constructs a prompt for GPT to classify speakers in a conversation.

    Args:
        sentences (List[str]): List of transcribed sentences.

    Returns:
        str: A formatted prompt instructing GPT to return speaker labels.
    """
    prompt = (
        "You are given a list of sentences from a conversation. "
        "Classify the speaker of each sentence as either 'robot' or 'user'.\n\n"
        "Sentences:\n"
    )
    for i, s in enumerate(sentences, 1):
        prompt += f"{i}. {s}\n"
    prompt += "\nReturn a JSON array like: [\"robot\", \"user\", ...]"
    return prompt

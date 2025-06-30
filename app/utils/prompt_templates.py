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

def generate_conversation_summary_prompt(conversation_text: str) -> str:
    """
    Constructs a prompt for GPT to generate a precise conversation summary.

    Args:
        conversation_text (str): The full text of the conversation.

    Returns:
        str: A formatted prompt instructing GPT to create a structured summary.
    """
    prompt = (
        "You are an expert in conversation analysis. Generate a structured summary of the following conversation.\n\n"
        "### Instructions:\n"
        "1. Create a concise but comprehensive title that captures the main topic of the conversation.\n"
        "2. Provide a detailed summary that includes:\n"
        "   - Key discussion points\n"
        "   - Important decisions made\n"
        "   - Action items discussed\n"
        "3. Extract and list specific user demands or points raised by the user.\n"
        "4. Format the output as a JSON object with the following structure:\n"
        "   {\n"
        "     \"title\": \"Concise title\",\n"
        "     \"summary\": \"Detailed summary...\",\n"
        "     \"user_demands_points\": [\"point 1\", \"point 2\", ...]\n"
        "   }\n\n"
        "### Conversation Text:\n"
        f"{conversation_text}\n\n"
        "### Output Format:\n"
        "Return ONLY the JSON object with the specified structure."
    )
    return prompt

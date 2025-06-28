import openai
import json
from typing import List
from app.utils.prompt_templates import generate_speaker_labeling_prompt

def label_speakers_using_openai(sentences: List[str]) -> List[str]:
    """
    Uses OpenAI GPT to classify each sentence as spoken by 'robot' or 'user'.

    Args:
        sentences (List[str]): List of sentences from the transcript.

    Returns:
        List[str]: Corresponding speaker labels ('robot' or 'user') for each sentence.
    """
    prompt = generate_speaker_labeling_prompt(sentences)

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a smart assistant that labels conversation roles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        print("label_speakers_using_openai error:", e)
        return ["robot" if i % 2 == 0 else "user" for i in range(len(sentences))]

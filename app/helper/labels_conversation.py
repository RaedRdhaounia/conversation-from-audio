import openai
import json
from typing import List

def label_speakers_using_openai(sentences: List[str]) -> List[str]:
    prompt = (
        "You are given a list of sentences from a conversation. "
        "Classify the speaker of each sentence as either 'robot' or 'user'.\n\n"
        "Sentences:\n"
    )
    for i, s in enumerate(sentences, 1):
        prompt += f"{i}. {s}\n"
    prompt += "\nReturn a JSON array like: [\"robot\", \"user\", ...]"

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

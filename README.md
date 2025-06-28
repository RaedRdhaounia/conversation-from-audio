# conversation-from-audio

A FastAPI-based backend service that takes a remote audio file (MP3/WAV) and returns a structured conversation with speaker labels (`robot` / `user`) and estimated durations per sentence.

> Ideal for processing call recordings into readable conversations.

---

## 🚀 Features

- 🎧 Accepts audio URL (MP3)
- 🤖 Transcribes speech using OpenAI Whisper
- 🧠 Splits into sentences with durations
- 🔈 Labels speakers (default alternating, future: Resemblyzer voice profiles)
- 📦 REST API powered by FastAPI

---

## 🧪 Live in Codespaces

You can open this repo directly in a [GitHub Codespace](https://github.com/features/codespaces) and it will run out of the box.

1. Click **Code > Codespaces > Create codespace**
2. After codespace boots, run:

```bash
cp .env.example .env
# Add your actual OpenAI key to .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

```

## 🔐 .env Setup
Copy .env.example and fill in your OpenAI API key:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
## 📦 Installation (Local Dev)

```bash
git clone https://github.com/RaedRdhaounia/conversation-from-audio
cd conversation-from-audio

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

uvicorn app.main:app --reload

```
## 📡 API Endpoint

### POST /api/conversation

This endpoint processes an audio URL to transcribe the conversation and identify speakers.

Request Body:
The request expects a JSON object with the following field:

Name	    | Type	 | Description
audio_url |	string | Public URL of the MP3 or WAV file

Example Request:

```bash 
POST http://localhost:8000/api/conversation
Content-Type: application/json

{
  "audio_url": "https://example.com/audio.mp3"
}
```

Response:
```json 
{
  "status": 200,
  "success": true,
  "message": "Transcription completed successfully.",
  "data": {
    "messages": [
      {
        "sender": "robot",
        "duration": 4,
        "text": "Bonjour, je suis ici pour vous aider..."
      },
      {
        "sender": "user",
        "duration": 4,
        "text": "Merci, je voudrais réserver une activité."
      }
    ]
  }
}
```

## 📁 Project Structure
conversation-from-audio/
├── .env.example
├── .gitignore
├── confitest.py
├── LICENSE
├── pytest.ini
├── README.md
├── app/
│   ├── api/
│   ├── core/
│   │   └── config.py
│   ├── helper/
│   │   ├── download_file.py
│   │   ├── duration_call.py
│   │   ├── labels_conversation.py
│   │   └── split_transcriptions.py
│   ├── models/
│   │   ├── conversation.py
│   │   └── response.py
│   ├── routes/
│   │   └── routes.py
│   ├── services/
│   │   ├── get_transcriptions.py
│   │   ├── speaker.py
│   │   └── transcriber.py
│   └── main.py
├── test/
│   ├── transcriber_test.py
│   └── .pytest_cache/
└── utils/
    ├── prompt_templates.py
    └── main.py


## ✅ Next Improvements
- 🎙️ Real speaker detection using Resemblyzer

- 🧪 Unit tests with mock audio

- 🐳 Docker deployment

- 🔐 API key auth or JWT

## development preview

[Development Preview](https://conversation-from-audio.onrender.com/)

## 👨‍💻 Maintainer

Made by @raedrdhaounia — contributions welcome!

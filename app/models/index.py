class IndexModel:
    def __init__(self):
        self.title = "Voice Transcriber Service"
        self.description = "Transform audio conversations into structured data and insights"
        self.services = [
            {
                "name": "Audio Processing",
                "description": "Transcribe audio files into text",
                "api_endpoint": "/docs#operation/process_audio",
                "example_response": {
                    "transcription": "The quick brown fox jumps over the lazy dog",
                    "confidence": 0.95
                }
            },
            {
                "name": "Summary Generation",
                "description": "Generate detailed summaries of conversations",
                "api_endpoint": "/docs#operation/generate_summary",
                "example_response": {
                    "title": "Project Planning Meeting",
                    "summary": "Team discussed project timeline and milestones",
                    "user_demands_points": [
                        "Need to finalize requirements by next week",
                        "Schedule sprint planning for Monday"
                    ]
                }
            }
        ]

def index():
    return IndexModel()

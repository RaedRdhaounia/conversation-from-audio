from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    app_name: str = "Voice Transcriber Service"
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    robot_profile_path: str = "data/robot_embed.npy"

    class Config:
        env_file = ".env"

settings = Settings()
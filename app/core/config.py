from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.

    Attributes:
        app_name (str): The name of the application.
        openai_api_key (str): API key for OpenAI services, loaded from the environment variable 'OPENAI_API_KEY'.
        robot_profile_path (str): File path to the robot embedding profile.
        audio_url (str): Default test audio URL, loaded from the environment variable 'TEST_AUDIO_URL'.

    Config:
        env_file (str): Path to the .env file containing environment variables.
    """
    app_name: str = "Voice Transcriber Service"
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    robot_profile_path: str = "data/robot_embed.npy"
    audio_url: str = Field(..., env="TEST_AUDIO_URL")

    class Config:
        env_file = ".env"

settings = Settings()

from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LLM Code Deployment"
    AIPIPE_API_KEY: str = ""  # AIpipe API key (OpenAI-compatible)
    GITHUB_TOKEN: str = ""
    SECRET_KEY: str = ""  # For validating student secrets
    
    class Config:
        env_file = ".env"

settings = Settings()
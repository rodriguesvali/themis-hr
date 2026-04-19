import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = os.getenv("APP_ENV", "development")
    backend_port: int = int(os.getenv("BACKEND_PORT", 8000))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./themis.db")
    crewai_model: str = os.getenv("CREWAI_MODEL", "gpt-4o-mini")
    crewai_provider: str = os.getenv("CREWAI_PROVIDER", "openai")
    knowledge_base_path: str = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = ".env"

settings = Settings()

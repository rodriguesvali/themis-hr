import os
from pathlib import Path

from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    app_env: str = os.getenv("APP_ENV", "development")
    backend_port: int = int(os.getenv("BACKEND_PORT", 8000))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./themis.db")
    crewai_model: str = os.getenv("CREWAI_MODEL", "gemini-3.1-pro-preview")
    crewai_provider: str = os.getenv("CREWAI_PROVIDER", "google")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    clt_pdf_path: str = os.getenv("CLT_PDF_PATH", "backend/docs/consolidacao_leis_trabalho.pdf")
    knowledge_base_path: str = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        env_file = str(PROJECT_ROOT / ".env")
        extra = "ignore" # Ignorar variáveis do .env que não usamos aqui como frontend_port

settings = Settings()

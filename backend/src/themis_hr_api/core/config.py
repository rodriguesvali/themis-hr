import logging
from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings


PROJECT_ROOT = Path(__file__).resolve().parents[4]
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    app_env: str = "development"
    backend_port: int = 8000
    database_url: str = "sqlite:///./themis.db"
    crewai_model: str = "gemini-3.1-pro-preview"
    crewai_provider: str = "google"
    google_api_key: str = ""
    gemini_api_key: str = ""
    clt_pdf_path: str = "backend/docs/consolidacao_leis_trabalho.pdf"
    knowledge_base_path: str = "./knowledge"
    log_level: str = "INFO"

    @model_validator(mode="after")
    def resolve_llm_key(self) -> "Settings":
        if self.google_api_key and self.gemini_api_key:
            logger.warning(
                "GOOGLE_API_KEY and GEMINI_API_KEY are both configured; "
                "using GOOGLE_API_KEY for this runtime."
            )
        elif self.gemini_api_key:
            self.google_api_key = self.gemini_api_key
            logger.warning(
                "GEMINI_API_KEY is configured without GOOGLE_API_KEY; "
                "using the legacy fallback. Prefer GOOGLE_API_KEY for demos."
            )

        return self

    class Config:
        env_file = str(PROJECT_ROOT / ".env")
        extra = "ignore" # Ignorar variáveis do .env que não usamos aqui como frontend_port

settings = Settings()

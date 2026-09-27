from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "DIVYAM"
    PROJECT_DESCRIPTION: str = "AI-Enabled Competency & Learning Platform for India's Official Statistical System (MoSPI)"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database: defaults to local SQLite, overridable via DATABASE_URL for Postgres
    DATABASE_URL: str = "sqlite:///./divyam.db"
    
    # AI / LLM Keys (Optional - gracefully falls back to deterministic local mock / heuristic parser)
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # Chroma Vector DB directory
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    # iGOT Karmayogi API Integration
    IGOT_API_BASE_URL: str = "https://karmayogi.gov.in/api/v1"
    IGOT_API_KEY: Optional[str] = None
    IGOT_SANDBOX_MODE: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()

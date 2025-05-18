from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Barbeque Nation Chatbot"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Database
    DATABASE_URL: Optional[str] = None
    
    # Knowledge Base
    KB_PATH: str = "data/knowledge_base"
    MAX_TOKENS: int = 800
    
    # State Machine
    TEMPLATES_PATH: str = "templates"
    
    # Post-Call Analysis
    ANALYSIS_EXPORT_PATH: str = "exports"

    # Knowledge Base
    KNOWLEDGE_BASE_PATH: str
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
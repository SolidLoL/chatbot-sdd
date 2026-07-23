from pydantic_settings import BaseSettings
from typing import List

# JWT_SECRET default: si no viene del entorno, se genera una clave aleatoria segura
import os
import secrets
_JWT_SECRET_DEFAULT = os.environ.get("JWT_SECRET", secrets.token_urlsafe(32))


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Chatbot SDD API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:4010"]

    # Databricks
    DATABRICKS_HOST: str = ""
    DATABRICKS_TOKEN: str = ""
    DATABRICKS_WAREHOUSE_ID: str = ""

    # Vector Search
    VECTOR_SEARCH_INDEX_NAME: str = "chatbot_docs"
    VECTOR_SEARCH_ENDPOINT_NAME: str = "vector_search_endpoint"

    # Model Serving
    MODEL_SERVING_ENDPOINT: str = ""

    # Auth
    JWT_SECRET: str = _JWT_SECRET_DEFAULT
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://chatbot:chatbot@localhost:5432/chatbot"

    # Demo mode — when True, auth returns a default user without requiring token
    DEMO_MODE: bool = True

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_WINDOW_SECONDS: float = 60.0

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
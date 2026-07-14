from pydantic_settings import BaseSettings
from typing import List


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
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
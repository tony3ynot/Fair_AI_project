from pydantic_settings import BaseSettings
from typing import List
import os
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fair AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://fairai_user:fair1234@mysql:3306/fair_ai_db?charset=utf8mb4"
    )
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
    
    class Config:
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS origins from environment variable if provided
        cors_origins_env = os.getenv("BACKEND_CORS_ORIGINS")
        if cors_origins_env:
            try:
                self.BACKEND_CORS_ORIGINS = json.loads(cors_origins_env)
            except json.JSONDecodeError:
                pass


settings = Settings()
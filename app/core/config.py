from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # App
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "DashAds Backend"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


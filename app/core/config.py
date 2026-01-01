from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database (Supabase PostgreSQL)
    DATABASE_URL: str
    
    # Supabase Configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # App Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "DashAds Backend"
    ENVIRONMENT: str = "development"
    
    # CORS (for production)
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "https://app.marketdash.com.br",
        "https://app-staging.marketdash.com.br",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


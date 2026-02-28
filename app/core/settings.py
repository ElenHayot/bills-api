from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List



class Settings(BaseSettings):
    """
    Central configuration of the application.
    Automatically loads from .env and environment variables.
    """
    # ===== VERSION =====
    version: str = "1.0.0"
    url_version: str = "v1"

    # ===== URL PREFIX =====
    url_prefix: str = "/api"

    # ===== Default pagination =====
    default_page_size: int = 10
    max_page_size: int = 100

    # ===== ENVIRONMENT =====
    environment: str = "development"
    debug: bool = False

    # ===== SECURITY =====
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    # ===== DATABASE =====
    database_url: str = "postgresql://postgres:postgres@localhost:5432/bills_db"

    # ===== CORS =====
    allow_credentials: bool=True
    allow_methods: List[str]=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers: List[str]=["*"]
    allowed_origins: List[str]=["http://localhost"]
    allowed_hosts: List[str]=["mon-domaine.com,www.mon-domaine.com"]

    # ===== SETTINGS CONFIG =====
    model_config = SettingsConfigDict(
        env_file=".env.development",
        case_sensitive=False,
        extra="ignore",
    )


    # ===== APP NAME =====
    app_name: str = f"Bills API ({version} - {environment})"
    app_description: str = "API for managing bills"
    app_license: str = "MIT"
    app_contact: str = "elen.hayot@gmail.com"
    app_www: str = "https://github.com/ElenHayot/bills-api"

@lru_cache
def get_settings() -> Settings:
    """
    Cache the settings so they are loaded only once.
    """
    return Settings()


settings = get_settings()
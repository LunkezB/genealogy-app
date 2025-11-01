from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BACKEND_PORT: int = 8000
    BACKEND_HOST: str = "0.0.0.0"
    DATABASE_URL: str
    CORS_ORIGINS: str = "*"


@lru_cache
def get_settings() -> Settings:
    return Settings()

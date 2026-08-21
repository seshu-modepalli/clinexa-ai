from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    HOST: str
    PORT: int

    MONGODB_URL: str
    DATABASE_NAME: str

    OLLAMA_URL: str
    OLLAMA_MODEL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    OTP_PROVIDER: str = "mock"
    OTP_EXPIRY_MINUTES: int = 5
    OTP_MAX_ATTEMPTS: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
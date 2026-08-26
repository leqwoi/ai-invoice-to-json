import os
from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "development"
    api_key: SecretStr = SecretStr("")

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVIRONMENT')}",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

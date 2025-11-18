from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_prefix="", case_sensitive=False)

    bot_token: SecretStr

    openai_api_key: SecretStr
    openai_model: str = "gpt-4o-mini"

    mongodb_uri: str
    database_name: str
    history_collection: str

    max_history_messages: int = 15
    system_prompt: str


def get_settings() -> Settings:
    return Settings()
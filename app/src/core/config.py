from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings"""

    project_name: str
    public_key: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.parent / ".env",
        extra="ignore",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


def _get_settings():
    return Settings()


settings = _get_settings()

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseModel):
    """Mongo DB settings"""

    url: str = "mongodb://localhost:27017"

class LogSettings(BaseModel):
    """Logging settings"""

    max_bytes: int = 100_000
    backup_count: int = 3
    file_name: str = "app.log"
    file_path: str = "./logs/"


class Settings(BaseSettings):
    """Project settings"""

    project_name: str
    default_host: str
    default_port: int

    page_number: int = 1
    page_size: int = 50

    public_key: str

    mongo: MongoSettings = MongoSettings()

    sentry_sdk_dsn: str

    log: LogSettings = LogSettings()

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent.parent / ".env",
        extra="ignore",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


def _get_settings() -> Settings:
    return Settings()


settings = _get_settings()
print(settings)
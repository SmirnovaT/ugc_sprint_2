from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Project settings"""

    project_name: str
    public_key: str


def _get_settings():
    load_dotenv()
    return Settings()


settings = _get_settings()

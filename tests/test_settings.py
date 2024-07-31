from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class TestSettings(BaseSettings):
    api_url: str = "http://api:8000"


def _get_settings() -> TestSettings:
    return TestSettings()


test_settings = _get_settings()

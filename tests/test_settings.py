from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class TestSettings(BaseSettings):
    api_url: str = "http://api:8000"
    private_key: str
    


def _get_settings() -> TestSettings:
    return TestSettings()


test_settings = _get_settings()

import asyncio
from typing import Any
from urllib.parse import urljoin

import aiohttp
import pytest

from test_settings import test_settings


@pytest.fixture(scope="session")
async def event_loop(request):
    """Event_loop для scope='session'"""

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client_session() -> aiohttp.ClientSession:
    """AIOHTTP - сессия"""

    client_session = aiohttp.ClientSession()
    yield client_session
    await client_session.close()


@pytest.fixture(scope="session")
async def make_post_request(client_session):
    """Отправка POST-запроса с AIOHTTP - сессией"""

    async def inner(endpoint: str, data: dict | None = None) -> tuple[Any, Any]:
        data = data or {}
        url = urljoin(test_settings.api_url, endpoint)
        async with client_session.post(url, json=data) as raw_response:
            response = await raw_response.json(content_type=None)
            status = raw_response.status
            return status, response

    return inner

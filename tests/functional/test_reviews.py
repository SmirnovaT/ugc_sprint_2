from http import HTTPStatus
from urllib.parse import urljoin

import pytest

from test_data.reviews import review_data
from test_settings import test_settings

EVENT_ENDPOINT = "/ugc/v1/reviews/"
EVENT_URL = urljoin(test_settings.api_url, EVENT_ENDPOINT)

pytestmark = pytest.mark.asyncio


async def test_review_success(client_session, make_post_request):
    status, response = await make_post_request(EVENT_URL, review_data)
    assert status == HTTPStatus.CREATED

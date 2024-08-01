from http import HTTPStatus
from urllib.parse import urljoin

import pytest

from test_data.reviews import review_data
from test_settings import test_settings

REVIEW_ENDPOINT = "/ugc/v1/reviews/"
REVIEW_URL = urljoin(test_settings.api_url, REVIEW_ENDPOINT)

pytestmark = pytest.mark.asyncio


async def test_review_success(client_session, make_post_request):
    status, response = await make_post_request(REVIEW_URL, review_data)
    assert status == HTTPStatus.CREATED


async def test_review_conflict(client_session, make_post_request):
    await make_post_request(REVIEW_URL, review_data)
    status, response = await make_post_request(REVIEW_URL, review_data)
    assert status == HTTPStatus.CONFLICT


async def test_get_reviews_success(client_session):
    url = f"{REVIEW_URL}??page%5Bsize%5D=50&page%5Bnumber%5D=1"
    async with client_session.get(url) as resp:
        assert resp.status == HTTPStatus.OK

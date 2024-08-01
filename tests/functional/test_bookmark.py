from http import HTTPStatus
from urllib.parse import urljoin

import pytest
from test_data.users import ADMIN_TOKEN_COOKIES
from test_settings import test_settings

BOOKMARK_ENDPOINT = "/ugc/v1/bookmarks/"
BOOKMARK_URL = urljoin(test_settings.api_url, BOOKMARK_ENDPOINT)

pytestmark = pytest.mark.asyncio


async def test_create_bookmark_success(client_session, make_post_request):
    url = f"{BOOKMARK_URL}?film_id=e5960b9e-e955-4a50-90f2-6d46cf608759"
    status, response = await make_post_request(url, cookies=ADMIN_TOKEN_COOKIES)
    assert status == HTTPStatus.CREATED


async def test_create_bookmark_unauthorized(client_session, make_post_request):
    url = f"{BOOKMARK_URL}?film_id=e5960b9e-e955-4a50-90f2-6d46cf608759"
    status, response = await make_post_request(url)
    assert status == HTTPStatus.FORBIDDEN


async def test_bookmark_conflict(client_session, make_admin_post_request):
    url = f"{BOOKMARK_URL}?film_id=e4960b9e-e955-4a50-90f2-6d46cf608759"
    await make_admin_post_request(url)
    status, response = await make_admin_post_request(url)
    assert status == HTTPStatus.CONFLICT


async def test_delete_bookmark_success(client_session, make_admin_post_request):
    url_post = f"{BOOKMARK_URL}?film_id=t5960b9e-e955-4a50-90f2-6d46cf608759"
    await make_admin_post_request(url_post)
    url_delete = f"{BOOKMARK_URL}?film_id=t5960b9e-e955-4a50-90f2-6d46cf608759"
    async with client_session.get(url_delete, cookies=ADMIN_TOKEN_COOKIES) as raw_response:
        assert raw_response.status == HTTPStatus.OK


async def test_get_bookmark_success(client_session, make_admin_post_request):
    url_post = f"{BOOKMARK_URL}?film_id=t5960b9e-e955-4a50-90f2-6d46cf608759"
    await make_admin_post_request(url_post)
    url_get = f"{BOOKMARK_URL}"
    async with client_session.get(url_get, cookies=ADMIN_TOKEN_COOKIES) as raw_response:
        assert raw_response.status == HTTPStatus.OK

import pytest_asyncio


def convert_bool(value: bool) -> str:
    return 'true' if value else 'false'


@pytest_asyncio.fixture()
async def notification_get_all(make_http_request, get_notification_api_url):
    async def inner(token: str, unread_only: bool) -> dict:
        return await make_http_request(
            'GET',
            f'{get_notification_api_url}/',
            params={'unread_only': convert_bool(unread_only)},
            token=token
        )

    return inner


@pytest_asyncio.fixture()
async def notification_make_read(make_http_request, get_notification_api_url):
    async def inner(token: str, notification_ids: list[int]) -> dict:
        return await make_http_request(
            'PATCH',
            f'{get_notification_api_url}/read',
            data=notification_ids,
            token=token
        )

    return inner

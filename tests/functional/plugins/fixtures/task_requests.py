import pytest_asyncio


@pytest_asyncio.fixture()
async def tasks_get_all(make_http_request, get_task_api_url):
    async def inner(token: str) -> dict:
        return await make_http_request(
            'GET',
            f'{get_task_api_url}tasks',
            token=token
        )
    return inner


@pytest_asyncio.fixture()
async def tasks_get_one(make_http_request, get_task_api_url):
    async def inner(task_id: int, token: str) -> dict:
        return await make_http_request(
            'GET',
            f'{get_task_api_url}tasks/{task_id}',
            token=token
        )
    return inner


@pytest_asyncio.fixture()
async def tasks_post(make_http_request, get_task_api_url):
    async def inner(token: str, plan_id: int, data: dict) -> dict:
        return await make_http_request(
            'POST',
            f'{get_task_api_url}plans/{plan_id}/tasks',
            token=token,
            data=data
        )
    return inner


@pytest_asyncio.fixture()
async def tasks_patch(make_http_request, get_task_api_url):
    async def inner(token: str, task_id: int, data: dict) -> dict:
        return await make_http_request(
            'PATCH',
            f'{get_task_api_url}tasks/{task_id}',
            token=token,
            data=data
        )
    return inner


@pytest_asyncio.fixture()
async def tasks_delete(make_http_request, get_task_api_url):
    async def inner(token: str, task_id: int) -> dict:
        return await make_http_request(
            'DELETE',
            f'{get_task_api_url}/tasks/{task_id}',
            token=token
        )
    return inner

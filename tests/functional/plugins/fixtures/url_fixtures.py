import pytest
from functional.settings import test_settings


@pytest.fixture(scope='session')
def get_notification_api_url():
    return f'{test_settings.fastapi.url}/api/v1/notifications'


@pytest.fixture(scope='session')
def get_task_api_url():
    return f'{test_settings.fastapi.url}/api/v1/'

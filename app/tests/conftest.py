import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def pytest_sessionstart():
    """Запуск скрипта в начале тестирования"""
    pass


def pytest_sessionfinish():
    """Запуск скрипта в конце тестирования"""
    pass


@pytest.fixture(scope="session")
def root_url():
    return "http://127.0.0.1:8000/api/v1/"

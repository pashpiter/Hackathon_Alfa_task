import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def pytest_sessionstart():
    # Выполняйте ваш код здесь
    print("Запуск скрипта в начале тестирования")


def pytest_sessionfinish():
    # Выполняйте ваш код здесь
    print("\nЗапуск скрипта в конце тестирования")


@pytest.fixture(scope="session")
def root_url():
    return "http://127.0.0.1:8000/api/v1/"

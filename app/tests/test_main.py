from .conftest import client


def test_read_api_docs(root_url):
    """Проверка доступности документации"""
    response = client.get(f"{root_url}openapi.json")
    assert response.status_code == 200

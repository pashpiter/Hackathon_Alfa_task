from .conftest import client


def test_read_employees_without_token(root_url):
    """Проверка получения пользователя без предоставления токена"""
    response = client.get(f"{root_url}employees")
    assert response.status_code == 403
    assert response.json() == {
        "detail": "В заголовке http запроса отсутствует Bearer токен"
    }

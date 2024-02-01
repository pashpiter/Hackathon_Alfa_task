from .conftest import client
# import db.fill_table_users as fill_table_users


def test_read_employees_without_token(root_url):
    response = client.get(f"{root_url}employees")
    assert response.status_code == 403
    assert response.json() == {
        "detail": "В заголовке http запроса отсутствует Bearer токен"
    }


# def test_read_employees_with_token(root_url):
#     response = client.get(f"{root_url}employees",
#                           headers={"Authorization": "Bearer token"})
#     assert response.status_code == 200

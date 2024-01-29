from api.v1.openapi.base import BaseOpenapi

get_employee = BaseOpenapi(
    summary="Получить информацию о сотруднике",
    description="",
    response_description=""
)

search_employees = BaseOpenapi(
    summary="Поиск сотрудников, относящихся к руководителю",
    description="Получение списка сотрудников относящихся к руководителю "
                "с возможностью фильтрации по ФИО. ",
    response_description=""
)

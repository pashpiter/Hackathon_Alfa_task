from api.v1.openapi.base import BaseOpenapi

get_task = BaseOpenapi(
    summary='Получить задачу',
    description='Получение задачи по id c комментариями.',
    response_description='Задача с комментариями'
)

get_tasks = BaseOpenapi(
    summary='Получить список задач',
    description='Получение списка задач относящихся к ИПР по ID плана.',
    response_description='Список задач ИПР'
)

create_task = BaseOpenapi(
    summary='Создать задачу',
    description='Создание задачи для ИПР. Доступ есть только у руководителя \
        сотрудника',
    response_description='Созданная задача'
)

update_task = BaseOpenapi(
    summary='Обновить задачу',
    description='Изменение задачи по ID. Доступ есть только у руководителя \
        сотрудника',
    response_description='Измененная задача'
)

delete_task = BaseOpenapi(
    summary='Удалить задачу',
    description='Удалить задачу по ID. Доступ есть только у руководителя \
        сотрудника'
)

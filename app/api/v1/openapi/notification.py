from api.v1.openapi.base import BaseOpenapi

get_notifications = BaseOpenapi(
    summary='Получить список уведомлений',
    description='',
    response_description=''
)

make_as_read = BaseOpenapi(
    summary='Пометить уведомления прочитанными',
    description='',
    response_description=''
)

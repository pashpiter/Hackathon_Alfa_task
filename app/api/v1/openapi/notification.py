from api.v1.openapi.base import BaseOpenapi

get_notifications = BaseOpenapi(
    summary='Получить список уведомлений',
    description=('Возвращает список всех уведомлений пользователя. Если '
                 'выставить unread_only=true, вернёт только непрочитанные '
                 'уведомления'),
    response_description='Список уведомлений (всех или только непрочитанных)'
)

read_notifications = BaseOpenapi(
    summary='Пометить уведомления прочитанными',
    description='Помечает все уведомления с заданными id прочитанными',
    response_description=''
)

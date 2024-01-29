# flake8: noqa: E501
from http import HTTPStatus

from fastapi import APIRouter, Depends, Query

from api.v1 import openapi
from core.logger import logger_factory
from db.crud import notification_crud
from db.database import AsyncSession, get_async_session
from schemas.notification import PK_TYPE, NotificationRead
from services.user import User, get_user

logger = logger_factory(__name__)

router = APIRouter(prefix='/notifications')


@router.get(
    '/',
    response_model=list[NotificationRead],
    **openapi.notification.get_notifications.model_dump()
)
async def get_notifications(
        user: User = Depends(get_user),
        unread_only: bool = Query(False),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка уведомлений."""
    attrs = {'recipient_id': user.id}
    if unread_only:
        attrs.update({'is_read': False})

    return await notification_crud.get_all(
        session,
        attrs,
        sort='created_at desc'
    )


@router.patch(
    '/read',
    status_code=HTTPStatus.NO_CONTENT,
    **openapi.notification.read_notifications.model_dump()
)
async def read_notifications(
        notification_ids: list[PK_TYPE],
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Групповое обновление уведомлений (делает их прочитанными)."""
    await notification_crud.make_read(session, user.id, notification_ids)

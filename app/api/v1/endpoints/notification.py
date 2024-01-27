# flake8: noqa: E501
from http import HTTPStatus

from fastapi import APIRouter, Depends

from api.v1 import openapi
from core.logger import logger_factory
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
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка уведомлений."""
    pass


@router.patch(
    '/read',
    status_code=HTTPStatus.NO_CONTENT,
    **openapi.notification.make_as_read.model_dump()
)
async def make_as_read(
        notification_ids: list[PK_TYPE],
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Групповое обновление уведомлений (делает их прочитанными)."""
    pass

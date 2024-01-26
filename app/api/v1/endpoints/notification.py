# flake8: noqa: E501
from http import HTTPStatus

from fastapi import APIRouter, Depends
from api.v1 import openapi
from core.logger import logger_factory
from db.database import AsyncSession, get_async_session
from schemas.notification import NotificationRead

logger = logger_factory(__name__)

router = APIRouter(prefix='/notifications')


@router.get(
    '/',
    response_model=list[NotificationRead],
    **openapi.notification.get_notifications.model_dump()
)
async def get_notifications(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка уведомлений."""
    pass

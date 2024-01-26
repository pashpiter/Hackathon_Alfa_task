# flake8: noqa: E501
from http import HTTPStatus

from fastapi import APIRouter, Depends
from api.v1 import openapi
from core.logger import logger_factory
from db.database import AsyncSession, get_async_session
from schemas.comment import CommentRead, CommentCreate

logger = logger_factory(__name__)

router = APIRouter(prefix='/{task_id}/comments')


@router.get(
    '/',
    response_model=list[CommentRead],
    **openapi.comment.get_comments.model_dump()
)
async def get_comments(
        plan_id: int,
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка комментариев"""
    pass


@router.post(
    '/',
    response_model=list[CommentRead],
    **openapi.comment.create_comment.model_dump()
)
async def create_comment(
        plan_id: int,
        task_id: int,
        comment_create: CommentCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание комментария"""
    pass

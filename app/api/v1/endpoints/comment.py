# flake8: noqa: E501
from http import HTTPStatus

import aiofiles
from fastapi import APIRouter, Depends, UploadFile

from api.v1 import openapi, validators
from core.config import ATTACHMENT, ATTACHMENT_DIR, STATIC
from core.logger import logger_factory
from core.utils import create_mock_file
from db.crud import comment_crud, unread_comment_crud
from db.database import AsyncSession, get_async_session
from schemas.base import PK_TYPE
from schemas.comment import CommentCreate, CommentRead
from services.user import User, get_user

logger = logger_factory(__name__)

router = APIRouter()


@router.get(
    "/tasks/{task_id}/comments",
    response_model=list[CommentRead],
    **openapi.comment.get_comments.model_dump()
)
async def get_comments(
        task_id: PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка комментариев."""
    await validators.check_task_and_user_access(task_id, user.id, session)
    return await comment_crud.get_all(
        session,
        user,
        {'task_id': task_id},
        sort='created_at desc'
    )


@router.post(
    "/tasks/{task_id}/comments",
    status_code=HTTPStatus.NO_CONTENT,
    **openapi.comment.create_comment.model_dump()
)
async def create_comment(
        task_id: PK_TYPE,
        comment: CommentCreate,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Создание комментария."""
    task = await validators.check_task_and_user_access(
        task_id, user.id, session
    )
    await comment_crud.create(
        session,
        user,
        task,
        {
            **comment.model_dump(),
            'task_id': task_id,
            'author_id': user.id
        }
    )


@router.post(
    "/tasks/{task_id}/upload",
    response_model=str,
    **openapi.comment.upload_file.model_dump()
)
async def upload_file(
        task_id: PK_TYPE,
        file: UploadFile,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Загрузка файла. Возвращает путь к загруженному файлу."""
    await validators.check_task_and_user_access(task_id, user.id, session)

    task_directory = ATTACHMENT_DIR / f'task_{task_id}'
    filename = create_mock_file(task_directory, file.filename)
    filepath = task_directory / filename

    async with aiofiles.open(filepath, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return f'{STATIC}/{ATTACHMENT}/task_{task_id}/{filename}'


@router.get(
    "/comments/unread",
    response_model=int,
    **openapi.comment.get_comments.model_dump()
)
async def get_unread_comments_amount(
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение количества непрочитанных комментариев."""
    return await unread_comment_crud.get_amount(session, user)

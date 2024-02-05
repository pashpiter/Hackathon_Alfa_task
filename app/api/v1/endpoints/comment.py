from http import HTTPStatus

import aiofiles
from fastapi import APIRouter, Depends, UploadFile

from api.v1 import openapi, validators
from core.config import ATTACHMENT, ATTACHMENT_DIR, STATIC
from core.logger import logger_factory
from core.utils import create_empty_file
from db.crud import comment_crud, notification_crud, unread_comment_crud
from db.database import AsyncSession, get_async_session
from schemas.base import PK_TYPE
from schemas.comment import CommentCreate, CommentRead
from schemas.notification import NotificationHeader, NotificationType
from services.user import User, get_user

logger = logger_factory(__name__)

router = APIRouter()

NEW_COMMENT = '{author} {task}'


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

    # сбрасываем счётчик непрочитанных комментариев у пользователя
    await unread_comment_crud.delete(
        session, {'reader_id': user.id, 'task_id': task_id}
    )

    # помечаем уведомления о новых комментариях к задаче прочитанными
    await notification_crud.update(
        session,
        {
            'recipient_id': user.id,
            'task_id': task_id,
            'header': NotificationHeader.COMMENT_NEW,
            'is_read': False
        },
        {'is_read': True}
    )

    return await comment_crud.get_all(
        session,
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

    reader_ids = [
        user.supervisor_id if user.supervisor_id else task.plan.employee_id
    ]

    # увеличиваем счётчик непрочитанных комментариев у всех пользователей,
    # связанных с задачей, за исключением автора комментария
    await unread_comment_crud.increase_counter(session, task_id, reader_ids)

    # создаём уведомление о новом комментарии у всех пользователей, связанных
    # с задачей, за исключением автора комментария.
    for reader_id in reader_ids:
        unread_notification = await notification_crud.get(
            session,
            {
                'recipient_id': reader_id,
                'task_id': task_id,
                'header': NotificationHeader.COMMENT_NEW,
                'is_read': False
            }
        )
        # если у пользователя уже висит непрочитанное уведомление о новом
        # комментарии, тогда ещё одного уведомления не создаём
        if unread_notification is None:
            await notification_crud.create(
                session,
                {
                    'recipient_id': reader_id,
                    'task_id': task_id,
                    'type': NotificationType.COMMON,
                    'header': NotificationHeader.COMMENT_NEW,
                    'content': NEW_COMMENT.format(
                        author=user.short_name,
                        task=task.name
                    )
                }
            )

    await comment_crud.create(
        session,
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
    filename = create_empty_file(task_directory, file.filename)
    filepath = task_directory / filename

    async with aiofiles.open(filepath, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    return f'{STATIC}/{ATTACHMENT}/task_{task_id}/{filename}'


@router.get(
    "/comments/unread",
    response_model=int,
    **openapi.comment.get_unread_comments_amount.model_dump()
)
async def get_unread_comments_amount(
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение количества непрочитанных комментариев."""
    return await unread_comment_crud.get_amount(session, user)

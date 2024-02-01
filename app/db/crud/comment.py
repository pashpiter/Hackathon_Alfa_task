from typing import Any, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import logger_factory
from db.crud.base import CRUDBase, ModelType
from schemas import Comment, Task, UnreadComment, User


class CRUDComment(CRUDBase):
    async def get_all(
            self,
            session: AsyncSession,
            reader: User,
            attrs: dict[str, Any] | None = None,
            *,
            limit: int | None = None,
            offset: int | None = None,
            sort: str | None = None,
            unique: bool = False
    ) -> Sequence[ModelType]:
        # сбрасываем счётчик непрочитанных комментариев у пользователя
        await unread_comment_crud.delete(
            session, {'reader_id': reader.id, 'task_id': attrs['task_id']}
        )
        return await super().get_all(
            session,
            attrs,
            limit=limit,
            offset=offset,
            sort=sort,
            unique=unique
        )

    async def create(
            self,
            session: AsyncSession,
            author: User,
            task: Task,
            obj_in: dict[str, Any] | ModelType,
    ) -> ModelType:
        # увеличиваем счётчик непрочитанных комментариев у всех пользователей,
        # имеющих доступ к комментариям (за исключением автора комментария)
        reader_id = author.supervisor_id if author.supervisor_id else task.plan.employee_id  # noqa:E501

        unread_comments = await unread_comment_crud.get(
            session,
            {'reader_id': reader_id, 'task_id': task.id}
        )
        if unread_comments is None:
            await unread_comment_crud.create(
                session,
                {'reader_id': reader_id, 'task_id': task.id, 'amount': 1}
            )
        else:
            unread_comments.amount += 1
            session.add(unread_comments)
            await session.commit()

        return await super().create(session, obj_in=obj_in)


class CRUDUnreadComment(CRUDBase):
    async def get_unread_amount(
            self,
            session: AsyncSession,
            user: User
    ):
        query = select(
            func.sum(self.model.amount)
        ).filter(
            self.model.reader_id == user.id
        )
        result = await session.execute(query)
        return result.scalars().first() or 0


comment_crud = CRUDComment(Comment, logger_factory(__name__))
unread_comment_crud = CRUDUnreadComment(UnreadComment, logger_factory(__name__))  # noqa:E501

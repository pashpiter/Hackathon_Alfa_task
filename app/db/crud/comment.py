from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logger import logger_factory
from db.crud.base import CRUDBase
from schemas import PK_TYPE, USER_PK_TYPE, Comment, UnreadComment, User


class CRUDComment(CRUDBase):
    pass


class CRUDUnreadComment(CRUDBase):
    async def increase_counter(
            self,
            session: AsyncSession,
            task_id: PK_TYPE,
            reader_ids: list[USER_PK_TYPE]
    ):
        """Увеличивает счётчик непрочитанных комментариев для задачи task_id у
        всех пользователей из списка reader_ids."""
        for reader_id in reader_ids:
            unread_comments = await unread_comment_crud.get(
                session,
                {'reader_id': reader_id, 'task_id': task_id}
            )
            if unread_comments is None:
                session.add(
                    self.model(
                        reader_id=reader_id,
                        task_id=task_id,
                        amount=1
                    )
                )
            else:
                unread_comments.amount += 1
                session.add(unread_comments)

        await session.commit()

    async def get_amount(
            self,
            session: AsyncSession,
            user: User
    ):
        """Возвращает количество непрочитанных комментариев пользователя по
        всем задачам, к которым он имеет отношение."""
        query = select(
            func.sum(self.model.amount)
        ).filter(
            self.model.reader_id == user.id
        )
        result = await session.execute(query)
        return result.scalars().first() or 0


comment_crud = CRUDComment(Comment, logger_factory(__name__))
unread_comment_crud = CRUDUnreadComment(UnreadComment, logger_factory(__name__))  # noqa:E501

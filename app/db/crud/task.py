from sqlmodel import Sequence
from core.logger import logger_factory
from db.crud.base import CRUDBase
from schemas import Task
from .base import ModelType, AsyncSession, Any

from sqlalchemy import update
from sqlalchemy.orm import selectinload


class CRUDTask(CRUDBase):

    async def update_many(
            self,
            session: AsyncSession,
            task_ids: list[int],
            obj_in: dict[str, Any]
    ) -> Sequence[ModelType]:
        """Обновляет все записи в БД, c id из списка task_ids.
        Словарь obj_in содержит обновляемые поля и их значения."""
        self.logger.debug(
            'UPDATE_ALL: model={}, task_ids={}, obj_in={}'.format(
                self.model, task_ids, obj_in)
        )

        if not isinstance(obj_in, dict):
            msg = 'Source object should be of type dict'
            self.logger.error(msg)
            raise ValueError(msg)

        query = update(self.model).where(Task.id.in_(task_ids)).values(
            **obj_in).returning(Task).options(selectinload(Task.plan))
        db_objs = await session.execute(query)
        await session.commit()
        return db_objs.unique().scalars().all()


task_crud = CRUDTask(Task, logger_factory(__name__))

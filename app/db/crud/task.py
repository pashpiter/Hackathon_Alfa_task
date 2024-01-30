from typing import Any, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from .base import ModelType
from core.logger import logger_factory
from db.crud.base import CRUDBase
from schemas import Task


class CRUDTask(CRUDBase):

    async def get_all_tasks(
            self,
            session: AsyncSession,
            attrs: dict[str, Any] | None = None,
            *, limit: int | None = None,
            offset: int | None = None,
            sort: str | None = None
    ) -> Sequence[ModelType]:
        self.logger.debug(f'GET_ALL: model={self.model}, attrs={attrs}')

        db_objs = await session.execute(
            self._make_query(attrs, limit=limit, offset=offset, sort=sort)
        )
        return db_objs.unique().scalars().all()


task_crud = CRUDTask(Task, logger_factory(__name__))

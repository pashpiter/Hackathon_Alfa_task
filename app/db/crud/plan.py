from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.exceptions import NotFoundException
from core.logger import logger_factory
from db.crud.base import CRUDBase
from schemas import Plan, User


class CRUDPlan(CRUDBase):

    async def get_latest(
            self,
            session: AsyncSession,
            employee_id: int
    ) -> Plan:
        """Возвращает последний ИПР сотрудника по id."""

        self.logger.debug(f'GET_LATEST_PLAN: attrs=({employee_id=})')

        plans = await self.get_all(
            session,
            {"employee_id": employee_id},
            sort="id desc",
            unique=True
        )
        if not plans:
            raise NotFoundException(
                "У вас нет ИПР, завести ИПР может ваш руководитель."
            )
        return plans[0]

    async def get_employees(
            self,
            session: AsyncSession,
            supervisor_id: int
    ) -> List[Plan] | None:
        """Возвращает ИПР всех сотрудников по id руководителя."""

        self.logger.debug(f"GET_EMPLOYEE'S_PLANS: attrs=({supervisor_id=})")

        sub_query = select(User.id).where(User.supervisor_id == supervisor_id)
        query = select(Plan).where(Plan.employee_id.in_(sub_query))
        plans = await session.execute(query)
        return plans.unique().scalars().all()


plan_crud = CRUDPlan(model=Plan, logger=logger_factory(__name__))

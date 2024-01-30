from datetime import date

from core.exceptions import (ForbiddenException, IncorrectDate,
                             NotFoundException)
from db.crud import plan_crud, task_crud, user_crud
from db.database import AsyncSession
from schemas.base import PK_TYPE, USER_PK_TYPE
from schemas.user import User

TASK_NOT_FOUND = "Задачи с id={} не существует"
PLAN_NOT_FOUND = "Плана с id={} не существует"
ACCESS_DENIED = ("Можно смотреть только комментарии к задачам своего ИПР или "
                 "ИПР подчинённых")
ACCESS_EMPLOYEE_DENIED = "Доступ доступен только для руководителя"
PLAN_DATE_LS_TASK = "Срок задачи {} не может быть больше срока ИПР {}"


async def check_task_and_user_access(
        task_id: PK_TYPE,
        user_id: USER_PK_TYPE,
        session: AsyncSession
) -> None:
    """Проверяет наличие задачи и права доступа пользователя к ИПР. Доступ к
    ИПР есть у сотрудника, к чьему ИПР проверяется наличие доступа, и у
    руководителя сотрудника."""
    task = await task_crud.get(session, {"id": task_id})

    if task is None:
        raise NotFoundException(TASK_NOT_FOUND.format(task_id))

    plan = await plan_crud.get(session, {'id': task.plan_id})
    employee = await user_crud.get(session, {'id': plan.employee_id})

    if user_id not in [employee.id, employee.supervisor_id]:
        raise ForbiddenException(ACCESS_DENIED)


async def check_plan_and_user_access(
        plan_id: PK_TYPE,
        user_id: USER_PK_TYPE,
        session: AsyncSession
) -> None:
    """Проверяет наличие ИПР и права доступа пользователя. Доступ к
    ИПР есть у сотрудника, прикрепленного к плану и у руководителя
    сотрудника."""
    plan = await plan_crud.get(session, {"id": plan_id})
    if plan is None:
        raise NotFoundException(PLAN_NOT_FOUND.format(plan_id))

    if user_id == plan.employee_id:
        return
    employee = await user_crud.get(session, {"id": plan.employee_id})

    if user_id != employee.supervisor_id:
        raise ForbiddenException(ACCESS_DENIED)


async def check_role(
        user: User
) -> None:
    """Проверка права доступа к эндпоинту.
    Доступ разрешен только для руководителя."""
    if user.supervisor_id:
        raise ForbiddenException(ACCESS_EMPLOYEE_DENIED)


async def check_plan_tasks_expired_date(
        session: AsyncSession,
        plan_id: PK_TYPE,
        date_in_task: date
) -> None:
    """Проверка что дата в задаче не превышает срок ИПР."""
    plan = await plan_crud.get(session, {"id": plan_id})
    if plan.expires_at < date_in_task:
        raise IncorrectDate(PLAN_DATE_LS_TASK.format(
            date_in_task, plan.expires_at
        ))

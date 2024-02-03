from datetime import date

from core.exceptions import (AlreadyExists, ForbiddenException, IncorrectDate,
                             NotFoundException)
from db.crud import plan_crud, task_crud, user_crud
from db.database import AsyncSession
from schemas.base import PK_TYPE, USER_PK_TYPE
from schemas.plan import Plan, PlanStatus
from schemas.task import Task
from schemas.user import User

TASK_NOT_FOUND = "Задачи с id={} не существует."
PLAN_NOT_FOUND = "Плана с id={} не существует."
USER_NOT_FOUND = "Пользователя с id={} не существует."
ACCESS_DENIED = ("Можно смотреть только комментарии к задачам своего ИПР или "
                 "ИПР подчинённых.")
ACCESS_EMPLOYEE_DENIED = "Доступ доступен только для руководителя."
PLAN_DATE_LS_TASK = "Срок задачи {} не может быть больше срока ИПР {}."
BANNED_SUPERVISOR_PLAN = "Руководителю нельзя назначить ИПР."
NOT_RELATED_EMPLOYEE = "Этот сотрудник относится к другому руководителю."
ACTIVE_PLAN_EXISTS = "У сотрудника в настоящий момент уже есть ИПР."
BANNED_DATE_REDUCE = "Нельзя уменьшить дату окончания ИПР."


async def check_task_and_user_access(
        task_id: PK_TYPE,
        user_id: USER_PK_TYPE,
        session: AsyncSession
) -> Task:
    """Проверяет наличие задачи и права доступа пользователя к ИПР. Доступ к
    ИПР есть у сотрудника, к чьему ИПР проверяется наличие доступа, и у
    руководителя сотрудника."""
    task = await task_crud.get(session, {"id": task_id})

    if task is None:
        raise NotFoundException(TASK_NOT_FOUND.format(task_id))

    if user_id in (task.plan.employee_id, task.plan.employee.supervisor_id):
        return task

    raise ForbiddenException(ACCESS_DENIED)


async def check_plan_and_user_access(
        plan_id: PK_TYPE,
        user_id: USER_PK_TYPE,
        session: AsyncSession
) -> Plan:
    """Проверяет наличие ИПР и права доступа пользователя. Доступ к
    ИПР есть у сотрудника, прикрепленного к плану и у руководителя
    сотрудника."""
    plan = await plan_crud.get(session, {"id": plan_id})

    if plan is None:
        raise NotFoundException(PLAN_NOT_FOUND.format(plan_id))

    if user_id in (plan.employee_id, plan.employee.supervisor_id):
        return plan

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
        plan: Plan,
        date_in_task: date
) -> None:
    """Проверка что дата в задаче не превышает срок ИПР."""
    if plan.expires_at < date_in_task:
        raise IncorrectDate(PLAN_DATE_LS_TASK.format(
            date_in_task, plan.expires_at
        ))


async def check_new_date_gt_current(
        element: Plan | Task,
        new_expires_date: date
) -> None:
    if new_expires_date < element.expires_at:
        raise IncorrectDate(BANNED_DATE_REDUCE)


async def check_employee_related_supervisor(
        supervisor_id: USER_PK_TYPE,
        employee_id: USER_PK_TYPE,
        session: AsyncSession
) -> None:
    employee = await user_crud.get(session, {"id": employee_id})

    if employee is None:
        raise NotFoundException(USER_NOT_FOUND.format(employee_id))

    if not employee.supervisor_id:
        raise ForbiddenException(BANNED_SUPERVISOR_PLAN)

    if employee.supervisor_id != supervisor_id:
        raise ForbiddenException(NOT_RELATED_EMPLOYEE)


async def check_no_active_plan(
        employee_id: USER_PK_TYPE,
        session: AsyncSession
) -> None:
    plans = await plan_crud.get_all(
        session,
        {"employee_id": employee_id},
        unique=True
    )
    if any(plan.status in (
        PlanStatus.CREATED, PlanStatus.IN_PROGRESS
    ) for plan in plans):
        raise AlreadyExists(ACTIVE_PLAN_EXISTS)

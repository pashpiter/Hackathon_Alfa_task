# flake8: noqa: E501
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from api.v1 import openapi, validators
from core.logger import logger_factory
from db.crud import plan_crud
from db.database import AsyncSession, get_async_session
from schemas.base import PK_TYPE
from schemas.plan import PlanCreate, PlanRead, PlanReadWithTasks, PlanUpdate
from services.user import User, get_user

logger = logger_factory(__name__)

router = APIRouter(prefix='/plans')


@router.get(
    '/{plan_id}',
    response_model=PlanReadWithTasks,
    **openapi.plan.get_plan.model_dump()
)
async def get_plan(
        plan_id: PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение ИПР по id."""
    await validators.check_plan_and_user_access(plan_id, user.id, session)
    return await plan_crud.get(session, {"id": plan_id})


@router.get(
    '/',
    response_model=list[PlanRead],
    **openapi.plan.get_plans.model_dump()
)
async def get_plans(
        request: Request,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session)
):
    """Получение списка ИПР.
    Руководитель получает все ИПР своих сотрудников.
    Сотрудник редиректится на свой последний ИПР.
    """
    if user.supervisor_id:
        plan = await plan_crud.get_latest(session, user.id)
        return RedirectResponse(f"{request.url._url}{plan.id}")
    return await plan_crud.get_employees(session, user.id)


@router.post(
    '/',
    response_model=PlanRead,
    **openapi.plan.create_plan.model_dump()
)
async def create_plan(
        plan_create: PlanCreate,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Создание ИПР."""
    await validators.check_role(user)
    await validators.check_employee_related_supervisor(
        user.id, plan_create.employee_id, session
    )
    await validators.check_no_active_plan(plan_create.employee_id, session)
    return await plan_crud.create(session, plan_create.model_dump())


@router.patch(
    '/{plan_id}',
    response_model=PlanRead,
    **openapi.plan.update_plan.model_dump()
)
async def update_plan(
        plan_id: PK_TYPE,
        plan_update: PlanUpdate,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление ИПР."""
    await validators.check_role(user)
    await validators.check_plan_and_user_access(plan_id, user.id, session)
    new_plan = await plan_crud.update(
        session,
        {"id": plan_id},
        plan_update.model_dump(exclude_unset=True),
        unique=True
    )
    return new_plan[0]

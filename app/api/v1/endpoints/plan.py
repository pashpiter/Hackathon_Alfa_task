# flake8: noqa: E501
from http import HTTPStatus

from fastapi import APIRouter, Depends
from api.v1 import openapi
from core.logger import logger_factory
from db.database import AsyncSession, get_async_session
from schemas.plan import PlanRead, PlanCreate, PlanUpdate

logger = logger_factory(__name__)

router = APIRouter(prefix='/plans')


@router.get(
    '/{plan_id}',
    response_model=PlanRead,
    **openapi.plan.get_plan.model_dump()
)
async def get_plan(
        plan_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Получение ИПР по id"""
    pass


@router.get(
    '/',
    response_model=list[PlanRead],
    **openapi.plan.get_plans.model_dump()
)
async def get_plans(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка ИПРов"""
    pass


@router.post(
    '/',
    response_model=PlanRead,
    **openapi.plan.create_plan.model_dump()
)
async def create_plan(
        plan: PlanCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание ИПР"""
    pass


@router.patch(
    '/{plan_id}',
    response_model=PlanRead,
    **openapi.plan.update_plan.model_dump()
)
async def update_plan(
        plan_id: int,
        plan_update: PlanUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление ИПР"""
    pass
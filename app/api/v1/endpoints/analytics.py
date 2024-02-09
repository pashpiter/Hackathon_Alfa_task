from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.v1 import openapi, validators
from core.logger import logger_factory
from core.utils import get_status_statistic
from db.crud import plan_crud
from db.database import AsyncSession, get_async_session
from schemas.plan import PlanStatus
from schemas.task import TaskStatus
from services.user import User, get_user

logger = logger_factory(__name__)

router = APIRouter()


@router.get("/analytics",
            response_class=JSONResponse,
            status_code=HTTPStatus.OK,
            **openapi.analytics.get_analytic.model_dump())
async def get_analytic(
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Эндпоинт для возврата статистики руководителя по планам и задачам"""
    await validators.check_role(user)
    plans = await plan_crud.get_employees(session, user.id)
    tasks = (task for plan in plans for task in plan.tasks)

    return {
        "plans": get_status_statistic(tasks, TaskStatus),
        "tasks": get_status_statistic(plans, PlanStatus)
    }

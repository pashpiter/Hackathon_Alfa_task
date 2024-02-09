from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.v1 import openapi, validators
from core.logger import logger_factory
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
    tasks = [task for plan in plans for task in plan.tasks]

    # Расчеты параметров для задач
    statuses_tasks = {}
    for status in TaskStatus:
        statuses_tasks[status.value] = sum(
            1 for task in tasks if task.status == status)
    result_tasks = {
        "total": len(tasks),
        "expired": statuses_tasks.get(TaskStatus.FAILED),
        "statuses": {
            "Создано": statuses_tasks.get(TaskStatus.CREATED),
            "Не выполнено": statuses_tasks.get(TaskStatus.FAILED),
            "В работе": statuses_tasks.get(TaskStatus.IN_PROGRESS),
            "На проверке": statuses_tasks.get(TaskStatus.UNDER_REVIEW),
            "Выполнено": statuses_tasks.get(TaskStatus.DONE),
        },
        "complete_percentage": '{}%'.format(
            statuses_tasks.get(TaskStatus.DONE)//len(tasks))
    }

    # Расчеты параметров для планов
    statuses_plans = {}
    for status in PlanStatus:
        statuses_plans[status.value] = sum(
            1 for plan in tasks if plan.status == status)
    result_plans = {
        "total": len(plans),
        "statuses": {
            "Создано": statuses_plans.get(PlanStatus.CREATED),
            "Не выполнено": statuses_plans.get(PlanStatus.FAILED),
            "В работе": statuses_plans.get(PlanStatus.IN_PROGRESS),
            "Выполнено": statuses_plans.get(PlanStatus.DONE),
        },
        "complete_percentage": '{}%'.format(
            statuses_plans.get(TaskStatus.DONE)//len(tasks))
    }

    return {
        "tasks": result_tasks,
        "plans": result_plans
    }

# flake8: noqa: E501
from http import HTTPStatus

from fastapi import APIRouter, Depends
from api.v1 import openapi
from core.logger import logger_factory
from db.database import AsyncSession, get_async_session
from schemas.task import TaskRead, TaskCreate, TaskUpdate

logger = logger_factory(__name__)

router = APIRouter(prefix="/plans/{plan_id}/tasks")


@router.get(
    '/{task_id}',
    response_model=TaskRead,
    **openapi.task.get_task.model_dump()
)
async def get_task(
        plan_id: int,
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Получение задачи по id."""
    pass


@router.get(
    '/',
    response_model=list[TaskRead],
    **openapi.task.get_tasks.model_dump()
)
async def get_tasks(
        plan_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка задач."""
    pass


@router.post(
    '/',
    response_model=TaskRead,
    **openapi.task.create_task.model_dump()
)
async def create_task(
        plan_id: int,
        task_create: TaskCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание задачи."""
    pass


@router.patch(
    '/{task_id}',
    response_model=TaskRead,
    **openapi.task.update_task.model_dump()
)
async def update_task(
        plan_id: int,
        task_id: int,
        task_patch: TaskUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление задачи."""
    pass


@router.delete(
    '/{task_id}',
    status_code=HTTPStatus.NO_CONTENT,
    **openapi.task.delete_task.model_dump()
)
async def delete_task(
        plan_id: int,
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление задачи."""
    pass

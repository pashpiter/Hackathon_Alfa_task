# flake8: noqa: E501
from datetime import date
from http import HTTPStatus
from typing import Union

from api.v1 import openapi, validators
from core.logger import logger_factory
from db.crud import comment_crud, plan_crud, task_crud
from db.database import AsyncSession, get_async_session
from fastapi import APIRouter, Depends
from schemas.base import PK_TYPE
from schemas.comment import CommentType
from schemas.plan import PlanStatus
from schemas.task import (TaskCreate, TaskRead, TaskReadWithComments,
                          TaskStatus, TaskUpdate)
from services.user import User, get_user

logger = logger_factory(__name__)

router = APIRouter(prefix="/plans/{plan_id}/tasks")


@router.get(
    "/{task_id}",
    response_model=TaskReadWithComments,
    **openapi.task.get_task.model_dump()
)
async def get_task(
        plan_id: PK_TYPE,
        task_id: PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение задачи по id. Проверка и изменение статуса задачи и
    статуса плна"""
    await validators.check_task_and_user_access(task_id, user.id, session)
    task = await task_crud.get(
        session, {"id": task_id}
    )
    # Проверка статуса задачи и изменение статуса задачи и статуса плана
    if task.status == TaskStatus.CREATED and user.supervisor_id:
        task = await task_crud.update(
            session,
            {"id": task_id},
            {"status": TaskStatus.IN_PROGRESS}
        )
        await plan_crud.update(
            session,
            {"id": plan_id},
            {"status": PlanStatus.IN_PROGRESS}
        )
    return task


@router.get(
    "/",
    response_model=list[TaskRead],
    **openapi.task.get_tasks.model_dump()
)
async def get_tasks(
        plan_id: PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка задач."""
    await validators.check_plan_and_user_access(plan_id, user.id, session)
    return await task_crud.get_all_tasks(session, {"plan_id": plan_id,})


@router.post(
    "/",
    response_model=TaskRead,
    **openapi.task.create_task.model_dump()
)
async def create_task(
        plan_id: PK_TYPE,
        task_create: TaskCreate,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Создание задачи. Добавление нового нового комментарияк задаче."""
    await validators.check_plan_and_user_access(plan_id, user.id, session)
    await validators.check_role(user)
    if task_create.expires_at:
        await validators.check_plan_tasks_expired_date(
            session, plan_id, task_create.expires_at
        )
    task = await task_crud.create(
        session, {
        **task_create.model_dump(),
        "plan_id": plan_id
        }
    )
    # Добавление комментария с датой создания
    await comment_crud.create(session, {
        "task_id": task.id,
        "author_id": user.id,
        "type": CommentType.TEXT,
        "content": "Задача создана {}".format(
            date.today().strftime("%d.%m.%Y")
        )
    })
    return task


@router.patch(
    "/{task_id}",
    response_model=Union[TaskRead, list[TaskRead]],
    **openapi.task.update_task.model_dump()
)
async def update_task(
        plan_id: PK_TYPE,
        task_id: PK_TYPE,
        task_patch: TaskUpdate,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление задачи."""
    await validators.check_plan_and_user_access(plan_id, user.id, session)
    await validators.check_role(user)
    new_task = await task_crud.update(
        session,
        {"id": task_id},
        task_patch.model_dump(exclude_unset=True)
    )
    if len(new_task) > 1:
        return new_task
    return new_task[0]


@router.delete(
    "/{task_id}",
    status_code=HTTPStatus.NO_CONTENT,
    **openapi.task.delete_task.model_dump()
)
async def delete_task(
        plan_id: PK_TYPE,
        task_id: PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление задачи."""
    await validators.check_plan_and_user_access(plan_id, user.id, session)
    await validators.check_role(user)
    await task_crud.delete(session, {"id": task_id})

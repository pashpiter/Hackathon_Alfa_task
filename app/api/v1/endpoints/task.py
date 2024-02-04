from datetime import date
from http import HTTPStatus
from typing import Union

from fastapi import APIRouter, Depends

from api.v1 import openapi, validators
from core.logger import logger_factory
from db.crud import comment_crud, notification_crud, plan_crud, task_crud
from db.database import AsyncSession, get_async_session
from schemas.base import PK_TYPE
from schemas.comment import CommentType
from schemas.notification import NotificationHeader, NotificationType
from schemas.plan import PlanStatus
from schemas.task import (TaskCreate, TaskRead, TaskReadWithComments,
                          TaskStatus, TaskUpdate)
from services.user import User, get_user

logger = logger_factory(__name__)

router = APIRouter(prefix="")

TASK_NOTIFICATIONS: dict = {
    TaskStatus.DONE: {
        "type": NotificationType.SUCCESS,
        "header": NotificationHeader.TASK_DONE
    },
    TaskStatus.UNDER_REVIEW: {
        "type": NotificationType.COMMON,
        "header": NotificationHeader.TASK_REVIEW
    },
    TaskStatus.IN_PROGRESS: {
        "type": NotificationType.COMMON,
        "header": NotificationHeader.TASK_IN_PROGRESS
    },
}


@router.get(
    "/tasks/{task_id}",
    response_model=TaskReadWithComments,
    **openapi.task.get_task.model_dump()
)
async def get_task(
        task_id: PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение задачи по id. Проверка и изменение статуса задачи и
    статуса плна"""
    task = await validators.check_task_and_user_access(
        task_id, user.id, session
    )
    # Проверка статуса задачи и изменение статуса задачи и статуса плана
    if task.status == TaskStatus.CREATED and user.supervisor_id:
        task = (await task_crud.update(
            session,
            {"id": task_id},
            {"status": TaskStatus.IN_PROGRESS},
            unique=True
        ))[0]
        await plan_crud.update(
            session,
            {"id": task.plan_id},
            {"status": PlanStatus.IN_PROGRESS},
            unique=True
        )
    return task


@router.get(
    "/plans/{plan_id}/tasks",
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
    return await task_crud.get_all(
        session, {"plan_id": plan_id}, unique=True
    )


@router.post(
    "/plans/{plan_id}/tasks",
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
    plan = await validators.check_plan_and_user_access(
        plan_id, user.id, session
    )
    await validators.check_role(user)
    if task_create.expires_at:
        await validators.check_plan_tasks_expired_date(
            session, plan, task_create.expires_at
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
    # Изменение статуса плана, если он был DONE
    if plan.status == PlanStatus.DONE:
        plan_crud.update(
            session, {"id": plan_id}, {"status": PlanStatus.IN_PROGRESS}
        )
    # Добавление уведомления
    await notification_crud.create(
        session, {
            "recipient_id": plan.employee_id,
            "task_id": task.id,
            "type": NotificationType.COMMON,
            "header": NotificationHeader.TASK_NEW,
            "content": "{} {}".format(
                user.short_name, task.name
            )
        }
    )
    return task


@router.patch(
    "/tasks/{task_id}",
    response_model=Union[TaskRead, list[TaskRead]],
    **openapi.task.update_task.model_dump()
)
async def update_task(
        task_id: PK_TYPE,
        task_patch: TaskUpdate,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Обновление задачи."""
    task = await validators.check_task_and_user_access(
        task_id, user.id, session
    )
    # Проверка статуса, который сотрудник может изменить
    if not (
        task_patch.status == TaskStatus.UNDER_REVIEW
        and len(task_patch.model_fields_set) == 1  # noqa W503
        and user.supervisor_id  # noqa W503
        and task.status == TaskStatus.IN_PROGRESS):  # noqa W503
        await validators.check_role(user)
    if task_patch.expires_at:
        await validators.check_new_date_gt_current(
            task, task_patch.expires_at
        )
    new_task = (await task_crud.update(
        session,
        {"id": task_id},
        task_patch.model_dump(exclude_unset=True),
        unique=True
    ))[0]

    if task_patch.status == TaskStatus.DONE:
        # Проверка что все задачи имеют статус DONE
        tasks_not_done = await task_crud.get_all(
            session,
            {"plan_id": task.plan_id},
            unique=True)
        if sum(1 for task in tasks_not_done if
               task.get("status") != TaskStatus.DONE):
            plan_crud.update(
                session, {"id": task.plan_id}, {"status": PlanStatus.DONE}
            )

    if task_patch.status in TASK_NOTIFICATIONS:
        # Добавление уведомления об изменении статус задачи
        await notification_crud.create(
            session, {
                "recipient_id": task.plan.employee_id,
                "task_id": task.id,
                "content": "{} {}".format(
                    user.short_name, task.name
                ),
                **TASK_NOTIFICATIONS[task_patch.status]
            }
        )
    return new_task  # noqa R504


@router.delete(
    "/tasks/{task_id}",
    status_code=HTTPStatus.NO_CONTENT,
    **openapi.task.delete_task.model_dump()
)
async def delete_task(
        task_id: PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Удаление задачи."""
    await validators.check_task_and_user_access(task_id, user.id, session)
    await validators.check_role(user)
    await task_crud.delete(session, {"id": task_id})

import asyncio
from datetime import date, datetime

from sqlalchemy import and_, update
from sqlalchemy.orm import selectinload

from db.crud import notification_crud, task_crud
from db.database import async_session_factory
from schemas.notification import (Notification, NotificationHeader,
                                  NotificationType)
from schemas.plan import Plan, PlanStatus
from schemas.task import Task, TaskStatus

MIDNIGHT = datetime.strptime("00:00:00", "%H:%M:%S")


async def check_plans() -> []:
    """Проверка планов на истекший дедлайн. В случае если дедлайн прошел
    и план находится в статусе CREATED или IN_PROGRESS, статус плана изменяется
    на FAILED. После этого все статусы задач CREATED и IN_PROGRESS в изменных
    планах изменяются на FAILED"""

    async with async_session_factory() as session:
        query = update(Plan).where(and_(
            Plan.status.in_((PlanStatus.CREATED, PlanStatus.IN_PROGRESS)),
            Plan.expires_at < date.today())
        ).values({"status": PlanStatus.FAILED}).returning(Plan).options(  # fix
            selectinload(Plan.tasks))
        query_plans = await session.execute(query)
        await session.commit()
        plans = query_plans.unique().scalars().all()
        # Выбор задач со статусом "Создано" и "В работе" из просроченых планов
        tasks_ids = [
            task.id for plan in plans for task in plan.tasks if
            task.status in (TaskStatus.CREATED, TaskStatus.IN_PROGRESS)
        ]
        tasks = await task_crud.update_by_ids(session, tasks_ids,
                                              {"status": TaskStatus.FAILED})
    return tasks  # noqa: R504


async def check_tasks() -> []:
    """Проверка задач на истекший дедлайн. В случае если дедлайн истек, а
    статус задачи CREATED или IN_PROGRESS, то статус данной задачи
    изменяется на FAILED"""

    async with async_session_factory() as session:
        query = update(Task).where(and_(
            Task.status.in_((TaskStatus.CREATED, TaskStatus.IN_PROGRESS)),
            Task.expires_at < date.today())
        ).values({"status": TaskStatus.FAILED}).returning(Task).options(
            selectinload(Task.plan))
        tasks = await session.execute(query)
        await session.commit()
        return tasks.unique().scalars().all()


async def main() -> None:
    """Программа ждет до полуночи и запускает проверку статусов"""
    while True:
        tasks = await check_plans()
        tasks += await check_tasks()

        # Добавление уведомлений для всех изменных задач
        notifications = []
        for task in tasks:
            for recipient in (
                task.plan.employee_id, task.plan.employee.supervisor_id
            ):
                notifications.append(
                    Notification(
                        recipient_id=recipient,
                        task_id=task.id,
                        type=NotificationType.FAIL,
                        header=NotificationHeader.TASK_FAILED,
                        content="{} {}".format(
                            task.plan.employee.full_name,
                            task.name
                        )
                    )
                )
        if notifications:
            async with async_session_factory() as session:
                await notification_crud.create_many(
                    session, notifications
                )
        await asyncio.sleep((datetime.now() - MIDNIGHT).total_seconds())


if __name__ == "__main__":
    asyncio.run(main())

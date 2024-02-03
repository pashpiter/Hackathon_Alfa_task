import asyncio
from datetime import datetime

from sqlalchemy import text

from core.utils import name_compression
from db.crud import notification_crud, plan_crud
from db.database import async_session_factory
from schemas.notification import (Notification, NotificationHeader,
                                  NotificationType)

MIDNIGHT = datetime.strptime("00:00:00", "%H:%M:%S")


async def check_plans() -> []:
    """Проверка планов на истекший дедлайн. В случае если дедлайн прошел
    и план находится в статусе CREATED или IN_PROGRESS, статус плана изменяется
    на FAILED. После этого все статусы задач CREATED и IN_PROGRESS в изменных
    планах изменяются на FAILED"""

    async with async_session_factory() as session:
        sql = """WITH updated_plans AS(
                    UPDATE plans.plan SET status = 'FAILED'
                        WHERE plans.plan.status IN ('CREATED', 'IN_PROGRESS')
                            AND plans.plan.expires_at < NOW()
                    RETURNING plans.plan.id
                ),
                update_tasks AS(
                    UPDATE plans.task SET status = 'FAILED'
                        WHERE plans.task.plan_id IN
                            (SELECT * FROM updated_plans) AND
                            plans.task.status IN ('CREATED', 'IN_PROGRESS')
                    RETURNING task)
                SELECT * FROM update_tasks;"""
        tasks = await session.execute(text(sql))
        await session.commit()
        return tasks.scalars().all()


async def check_tasks() -> []:
    """Проверка задач на истекший дедлайн. В случае если дедлайн истек, а
    статус задачи CREATED или IN_PROGRESS, то статус данной задачи
    изменяется на FAILED"""

    async with async_session_factory() as session:
        sql = """UPDATE plans.task SET status = 'FAILED'
                    WHERE plans.task.status IN ('CREATED', 'IN_PROGRESS') AND
                        plans.task.expires_at < NOW()
                    RETURNING task;"""
        tasks = await session.execute(text(sql))
        await session.commit()
        return tasks.scalars().all()


async def main() -> None:
    """Программа ждет до полуночи и запускает проверку статусов"""
    while True:
        tasks = await check_plans()
        tasks += await check_tasks()

        # Добавление уведомлений для всех изменных задач
        notifications = []
        async with async_session_factory() as session:
            for task in tasks:
                plan = await plan_crud.get(
                    session, {"id": task.get("plan_id")}
                )
                for recipient in (
                    plan.employee_id, plan.employee.supervisor_id
                ):
                    notifications.append(
                        Notification(
                            recipient_id=recipient,
                            task_id=task.get("id"),
                            type=NotificationType.FAIL,
                            header=NotificationHeader.TASK_FAILED,
                            content="{} {}".format(
                                name_compression(plan.employee.full_name),
                                task.get("name")
                            )
                        )
                    )
        if notifications:
            await notification_crud.create_many(
                session, notifications
            )
        await asyncio.sleep((datetime.now() - MIDNIGHT).total_seconds())


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from datetime import datetime
from db.database import async_session_factory
from sqlalchemy import text

MIDNIGHT = datetime.strptime("00:00:00", "%H:%M:%S")


async def check_plans() -> None:
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
                )
                SELECT * FROM updated_plans;"""
        await session.execute(text(sql))
        await session.commit()


async def check_tasks() -> None:
    """Проверка задач на истекший дедлайн. В случае если дедлайн истек, а
    статус задачи CREATED или IN_PROGRESS, то статус данной задачи
    изменяется на FAILED"""

    async with async_session_factory() as session:
        sql = """UPDATE plans.task SET status = 'FAILED'
                    WHERE plans.task.status IN ('CREATED', 'IN_PROGRESS') AND
                        plans.task.expires_at < NOW();"""
        await session.execute(text(sql))
        await session.commit()


async def main():
    """Программа ждет до полуночи и запускает проверку статусов"""
    while True:
        await check_plans()
        await check_tasks()
        await asyncio.sleep((datetime.now() - MIDNIGHT).total_seconds())

if __name__ == "__main__":
    asyncio.run(main())

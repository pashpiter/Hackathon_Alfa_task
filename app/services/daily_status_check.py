import asyncio
from db.database import async_session_factory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi import Depends
from schemas.task import TaskStatus
from db.crud import task_crud, plan_crud
from datetime import date, datetime


async def check_plans():
    async with async_session_factory() as session:
        sql = """WITH updated_plans AS(
	                UPDATE plans.plan SET status = 'CREATED'
		                WHERE plans.plan.status IN ('DONE', 'IN_PROGRESS')
			                AND plans.plan.expires_at > NOW()
		            RETURNING plans.plan.id
                ),
                update_tasks AS(
                    UPDATE plans.task SET status = 'CREATED'
                        WHERE plans.task.plan_id IN
                            (SELECT * FROM updated_plans) AND
                            plans.task.status = 'FAILED')
                SELECT * FROM updated_plans;"""
        updated_plans_ids = await session.execute(text(sql))
        await session.commit()
        print(updated_plans_ids.scalars().all())


async def check_tasks():
    async with async_session_factory() as session:
        sql = """UPDATE plans.task SET status = 'CREATED'
                    WHERE plans.task.status IN ('IN_PROGRESS', 'FAILED') AND
                        plans.task.expires_at > NOW()
                    RETURNING plans.task.id;"""
        updated_tasks_ids = await session.execute(text(sql))
        await session.commit()
        print(updated_tasks_ids.scalars().all())


async def check_status():
    pass


async def main():
    # await check_plans()
    await check_tasks()

if __name__ == "__main__":
    asyncio.run(main())

from fastapi import APIRouter
from typing import Union
from app.plan.schemas import Plan, Task, User
from uuid import UUID
from datetime import date, datetime

# Роутер для ИПР
plan_router = APIRouter(prefix="/plans", tags=["Plans"])


@plan_router.get("/")
async def get_plans():
    """Получение списка ИПРов"""
    return {"plans": ['plan1', 'plan2', 'plan3']}


@plan_router.post("/")
async def create_plan(employee_id: UUID, aim: str, plan_completion_date: date):
    """Создание ИПР"""
    pass
    return {
        "employee": User,
        "aim": aim,
        "plan_completion_date": plan_completion_date
    }


@plan_router.get("/{plan_id}")
async def get_plan(plan_id: int):
    """Получение ИПР по id"""
    pass
    return {
        "plan_id": plan_id
    }


@plan_router.patch("/{plan_id}")
async def update_plan(plan_id: int, aim: str | None, plan_completion_date: date | None):
    """Обновление ИПР"""
    pass
    return {"plan_id": plan_id, "aim": aim, "plan_completion_date": plan_completion_date}


# Роутер для задач
task_router = APIRouter(tags=["Tasks"])


@task_router.get("/{plan_id}/tasks")
async def get_tasks(plan_id: int):
    """Получение списка задач"""
    return {
        "plan_id": plan_id,
        "tasks": ['task1', 'task2', 'task3'],
    }


@task_router.post("/{plan_id}/tasks")
async def create_task(
        plan_id: UUID,
        task_name: str,
        task_description: str,
        task_completion_date: date | None = datetime.now().date(),
):
    """Создание задачи"""
    return {
        "plan_id": plan_id,
        "task_name": task_name
    }


@task_router.get("/{plan_id}/tasks/{task_id}")
async def get_task(plan_id: int, task_id: int):
    """Получение задачи по id"""
    return {
        "plan_id": plan_id,
        "task_id": task_id
    }


@task_router.patch("/{plan_id}/tasks/{task_id}")
async def update_task(plan_id: int, task_id: int, task_name: str | None = None):
    """Обновление задачи"""
    pass
    return {
        "task_name": task_name,
    }


@task_router.delete("/{plan_id}/tasks/{task_id}")
async def delete_task(plan_id: int, task_id: int):
    """Удаление задачи"""
    pass
    return {
        "message": "Task deleted",
        "response_code": 200
    }

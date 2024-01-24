from fastapi import APIRouter
from typing import List, Optional
from app.plan.schemas import Plan, Task, User
from datetime import date, datetime, timedelta

# Роутер для ИПР
plan_router = APIRouter(prefix="/plans", tags=["Plans"])


@plan_router.get("/", response_model=List[Plan])
async def get_plans():
    """Получение списка ИПРов"""
    pass


@plan_router.post("/", response_model=Plan)
async def create_plan(
        employee_id: int,
        aim: str,
        plan_completion_date: date = datetime.now().date() + timedelta(days=180)
):
    """Создание ИПР"""
    pass


@plan_router.get("/{plan_id}", response_model=Plan)
async def get_plan(plan_id: int):
    """Получение ИПР по id"""
    pass


@plan_router.patch("/{plan_id}", response_model=Plan)
async def update_plan(plan_id: int, aim: Optional[str]):
    """Обновление ИПР"""
    pass


# Роутер для задач
task_router = APIRouter(tags=["Tasks"])


@task_router.get("/{plan_id}/tasks", response_model=Task)
async def get_tasks(plan_id: int):
    """Получение списка задач"""
    pass


@task_router.post("/{plan_id}/tasks", response_model=List[Task])
async def create_task(
        plan_id: int,
        task_name: str,
        task_description: str,
        task_completion_date: Optional[date] = datetime.now().date(),
):
    """Создание задачи"""
    pass


@task_router.get("/{plan_id}/tasks/{task_id}", response_model=Task)
async def get_task(plan_id: int, task_id: int):
    """Получение задачи по id"""
    pass


@task_router.patch("/{plan_id}/tasks/{task_id}", response_model=List[Task])
async def update_task(plan_id: int, task_id: int, task_name: Optional[str] = None):
    """Обновление задачи"""
    pass


@task_router.delete("/{plan_id}/tasks/{task_id}")
async def delete_task(plan_id: int, task_id: int):
    """Удаление задачи"""
    pass
    return {
        "message": "Task deleted",
        "response_code": 200
    }

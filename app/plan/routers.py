from typing import List

from fastapi import APIRouter

from app.plan.schemas import (Plan, PlanBase, PlanCreate, PlanRead, PlanUpdate,
                              Task, TaskBase, TaskCreate, TaskRead, TaskUpdate)


# Роутер для ИПР
plan_router = APIRouter(prefix="/plans", tags=["Plans"])
# Роутер для задач
task_router = APIRouter(prefix="/{plan_id}/tasks", tags=["Tasks"])


@plan_router.get("/", response_model=List[PlanRead])
async def get_plans():
    """Получение списка ИПРов"""
    pass


@plan_router.post("/", response_model=PlanRead)
async def create_plan(plan: PlanCreate):
    """Создание ИПР"""
    pass


@plan_router.get("/{plan_id}", response_model=PlanRead)
async def get_plan(plan_id: int):
    """Получение ИПР по id"""
    pass


@plan_router.patch("/{plan_id}", response_model=PlanRead)
async def update_plan(plan_id: int, plan_update: PlanUpdate):
    """Обновление ИПР"""
    pass


@task_router.get("/", response_model=List[TaskRead])
async def get_tasks(plan_id: int):
    """Получение списка задач"""
    pass


@task_router.post("/", response_model=TaskRead)
async def create_task(plan_id: int, task_create: TaskCreate):
    """Создание задачи"""
    pass


@task_router.get("/{task_id}", response_model=TaskRead)
async def get_task(plan_id: int, task_id: int):
    """Получение задачи по id"""
    pass


@task_router.patch("/task_id}", response_model=TaskRead)
async def update_task(plan_id: int, task_id: int, task_patch: TaskUpdate):
    """Обновление задачи"""
    pass


@task_router.delete("/{task_id}", status_code=204)
async def delete_task(plan_id: int, task_id: int):
    """Удаление задачи"""
    pass

plan_router.include_router(task_router)

from fastapi import APIRouter, Depends

from api.v1 import openapi, validators
from core.logger import logger_factory
from db.database import AsyncSession, get_async_session
from schemas.base import USER_PK_TYPE
from schemas.user import User, UserRead, UserReadWithSupervisor
from services.user import get_user
from db.crud.user import user_crud

logger = logger_factory(__name__)

router = APIRouter(prefix="/employees")


@router.get(
    "/{employee_id}",
    response_model=UserReadWithSupervisor,
    **openapi.employee.get_employee.model_dump()
)
async def get_employee(
        employee_id: USER_PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение информации о сотруднике"""
    # Валидация доступа
    await validators.check_role(user)
    # Проверка существования сотрудника
    return await validators.check_employee_related_supervisor(
        user.id, employee_id, session
    )


@router.get(
    "/",
    response_model=list[UserRead],
    **openapi.employee.search_employees.model_dump()
)
async def search_employees(
        user: User = Depends(get_user),
        full_name: str = None,
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка сотрудников относящихся к руководителю
    с возможностью фильтрации по ФИО. При full_name = 'аша' выдаются все
    пользователи в фио которых есть совпадения с 'аша'."""
    # Валидация доступа
    await validators.check_role(user)
    # Поиск сотрудников
    employees = await user_crud.get_all(
        session, attrs={"supervisor_id": user.id}
    )
    # Фильтрация по ФИО
    if full_name:
        f_name_lower = full_name.lower()
        return [x for x in employees if f_name_lower in x.full_name.lower()]
    return employees

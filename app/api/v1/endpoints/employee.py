from fastapi import APIRouter, Depends

from api.v1 import openapi, validators
from core.logger import logger_factory
from db.database import AsyncSession, get_async_session
from schemas.base import USER_PK_TYPE
from schemas.user import User, UserRead, UserReadWithSupervisor
from services.user import get_user

logger = logger_factory(__name__)

router = APIRouter(prefix='/employees')


@router.get(
    "/{employee_id}",
    response_model=UserReadWithSupervisor,
    **openapi.task.get_task.model_dump()
)
async def get_task(
        employee_id: USER_PK_TYPE,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получение сотрудника по id."""
    # Валидация доступа
    pass


@router.get(
    "/",
    response_model=list[UserRead],
    **openapi.task.get_tasks.model_dump()
)
async def get_tasks(
        user: User = Depends(get_user),
        full_name: str = None,
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка сотрудников относящихся к руководитлею
    с возможностью фильтрации по ФИО. При full_name = 'аша' выдаются все
    пользователи в фио которых есть совпадения с 'аша'."""
    # Валидация доступа
    pass

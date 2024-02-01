from http import HTTPStatus

from fastapi import Depends, Header, HTTPException

from db.crud import user_crud
from db.database import AsyncSession, get_async_session
from schemas.user import User
from core.config import Permissions
from api.v1.validators import ACCESS_EMPLOYEE_DENIED

MISSING_TOKEN = 'В заголовке http запроса отсутствует Bearer токен'
USER_NOT_FOUND = 'Пользователь не найден'


async def get_user(
        token: str | None = Header(default=None, alias='Authorization'),
        session: AsyncSession = Depends(get_async_session),
) -> User:
    """Функция проверки токена пользователя. Используется Bearer токен."""
    if token is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=MISSING_TOKEN
        )

    user = await user_crud.get(session, {'token': token.split()[-1]})
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=USER_NOT_FOUND
        )
    return user


class PermissionChecker:

    def __init__(self, permissions: list[str]) -> None:
        self.permissions = permissions

    def __call__(self, user: User = Depends(get_user)) -> User:
        if user.supervisor_id and (
            Permissions.EMPLOYEE not in self.permissions
        ):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail=ACCESS_EMPLOYEE_DENIED
            )
        return user

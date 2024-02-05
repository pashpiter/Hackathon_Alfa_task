from http import HTTPStatus

from fastapi import Depends, Header, HTTPException

from db.crud import user_crud
from db.database import AsyncSession, get_async_session
from schemas.user import User

MISSING_TOKEN = "В заголовке http запроса отсутствует Bearer токен"
USER_NOT_FOUND = "Пользователь с данным токеном не найден"


async def get_user(
        token: str | None = Header(default=None, alias="Authorization"),
        session: AsyncSession = Depends(get_async_session),
) -> User:
    """Функция проверки токена пользователя. Используется Bearer токен."""
    if token is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=MISSING_TOKEN
        )

    user = await user_crud.get(session, {"token": token.split()[-1]})
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=USER_NOT_FOUND
        )

    return user

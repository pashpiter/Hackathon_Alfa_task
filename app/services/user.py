from http import HTTPStatus

from schemas.user import User
from fastapi import Header, HTTPException, Depends
from db.database import AsyncSession, get_async_session
from db.crud import user_crud


async def get_user(
        token: str | None = Header(default=None, alias='Authorization'),
        session: AsyncSession = Depends(get_async_session),
) -> User:
    """Функция проверки токена пользователя. Используется Bearer токен."""
    if token is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Missing token in request header'
        )

    user = await user_crud.get(session, {'token': token.split()[-1]})
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="User isn't found"
        )

    return user

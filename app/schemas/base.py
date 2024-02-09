from datetime import date, datetime, timedelta
from http import HTTPStatus
from typing_extensions import Annotated

from fastapi import HTTPException
from pydantic.functional_validators import BeforeValidator

PK_TYPE = int
USER_PK_TYPE = int


def validate_expires_date(d: str | date) -> date:
    """Валидация для даты окончания ИПР / задачи в запросах POST, PATCH.
    Пример:
    https://docs.pydantic.dev/latest/concepts/validators/
    """
    if isinstance(d, str):
        d = datetime.strptime(d, "%d.%m.%Y").date()
    if d < date.today():
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Нельзя установить дату в прошлом."
        )
    elif d - date.today() < timedelta(days=1):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Дата окончания не может быть меньше одного дня."
        )
    return d


EXPIRES_DATE_TYPE = Annotated[date, BeforeValidator(validate_expires_date)]

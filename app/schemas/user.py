# flake8: noqa: VNE003
from typing import Optional

from pydantic import computed_field
from sqlmodel import Field, SQLModel

from core.config import settings
from schemas.base import USER_PK_TYPE


class UserBase(SQLModel):
    full_name: str
    position: str
    photo: Optional[str]

    @computed_field
    @property
    def short_name(self) -> str:
        """Возвращает сокращённый формат полного имени.
        Формат full_name -> результат:
        - Имя -> Имя
        - Имя Фамилия -> Фамилия И.
        - Фамилия Имя Отчество -> Фамилия И.О.
        """
        split_full_name = self.full_name.split()
        match len(split_full_name):
            case 1:
                return split_full_name[0]

            case 2:
                return f'{split_full_name[-1]} {split_full_name[0][0]}.'

            case _:
                return '{surname} {initials}.'.format(
                    surname=split_full_name[0],
                    initials='.'.join(name[0] for name in split_full_name[1:])
                )


class User(UserBase, table=True):
    __table_args__ = {"schema": settings.postgres.db_schema}

    id: Optional[USER_PK_TYPE] = Field(default=None, primary_key=True)
    token: str
    supervisor_id: Optional[int]


class UserRead(UserBase):
    id: int


class UserReadWithSupervisor(UserRead):
    supervisor: Optional[UserRead] = None

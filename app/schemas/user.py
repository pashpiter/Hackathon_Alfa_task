# flake8: noqa: VNE003
from typing import Optional

from sqlmodel import Field, SQLModel

from core.config import settings
from schemas.base import USER_PK_TYPE


class UserBase(SQLModel):
    full_name: str
    position: str


class User(UserBase, table=True):
    __table_args__ = {"schema": settings.postgres.db_schema}

    id: Optional[USER_PK_TYPE] = Field(default=None, primary_key=True)
    token: str
    supervisor_id: Optional[int]


class UserRead(UserBase):
    id: int


class UserReadWithSupervisor(UserRead):
    supervisor: Optional[UserRead] = None

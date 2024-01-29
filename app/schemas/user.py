# flake8: noqa: VNE003
from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from core.config import settings
from schemas.base import USER_PK_TYPE
if TYPE_CHECKING:
    from schemas.plan import Plan


class UserBase(SQLModel):
    full_name: str
    position: str


class User(UserBase, table=True):
    __table_args__ = {"schema": settings.postgres.db_schema}

    id: Optional[USER_PK_TYPE] = Field(default=None, primary_key=True)
    token: str
    supervisor_id: Optional[int]

    plan: Optional["Plan"] = Relationship(back_populates="employee")


class UserRead(UserBase):
    id: int


class UserReadWithSupervisor(UserBase):
    supervisor: Optional[UserRead] = None

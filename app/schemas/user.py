from sqlmodel import SQLModel, Field
from typing import Optional
from core.config import settings
from schemas.base import USER_PK_TYPE


class UserBase(SQLModel):
    full_name: str
    position: str


class User(UserBase, table=True):
    __table_args__ = {'schema': settings.postgres.schema}

    id: Optional[USER_PK_TYPE] = Field(default=None, primary_key=True)
    token: str
    supervisor_id: Optional[int]


class UserRead(UserBase):
    pass

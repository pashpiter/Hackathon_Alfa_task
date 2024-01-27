# flake8: noqa: VNE003
import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, text

from core.config import settings
from schemas.base import PK_TYPE, USER_PK_TYPE


class CommentType(str, enum.Enum):
    TEXT = 'text'
    FILE = 'file'
    LINK = 'link'


class CommentBase(SQLModel):
    task_id: PK_TYPE
    author_id: USER_PK_TYPE
    type: CommentType
    content: str


class Comment(CommentBase, table=True):
    __table_args__ = {'schema': settings.postgres.schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    task_id: PK_TYPE = Field(foreign_key='task.id')
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )


class CommentRead(CommentBase):
    id: PK_TYPE
    created_at: datetime


class CommentCreate(CommentBase):
    pass

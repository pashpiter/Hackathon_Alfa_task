from sqlmodel import SQLModel, Field, text, DateTime, Column
from typing import Optional
from datetime import datetime
import enum
from core.config import settings
from schemas.base import PK_TYPE, USER_PK_TYPE, PrimaryKey


class CommentType(str, enum.Enum):
    TEXT = 'text'
    FILE = 'file'
    LINK = 'link'


class CommentBase(SQLModel):
    pass


class Comment(CommentBase, PrimaryKey, table=True):
    __table_args__ = {'schema': settings.postgres.schema}

    task_id: PK_TYPE = Field(default=None, foreign_key='task.id')
    author_id: USER_PK_TYPE
    type: CommentType
    content: str
    is_read: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )


class CommentRead(CommentBase):
    pass


class CommentCreate(CommentBase):
    pass

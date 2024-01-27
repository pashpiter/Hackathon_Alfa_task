# flake8: noqa: VNE003
import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, text, Relationship

from core.config import settings
from schemas.base import PK_TYPE, USER_PK_TYPE
from pydantic import BaseModel, HttpUrl, model_validator
from schemas.user import UserRead, User

# Разделитель, используемый при записи ссылки в БД. В самой БД хранится в виде:
# <текст ссылки><РАЗДЕЛИТЕЛЬ><url ссылки>
SEPARATOR = '$'


class CommentType(str, enum.Enum):
    TEXT = 'text'
    FILE = 'file'
    LINK = 'link'


class Link(BaseModel):
    text: str
    url: HttpUrl

    def to_str(self) -> str:
        return f'{self.text}{SEPARATOR}{self.url}'

    @staticmethod
    def from_str(text_: str, url_: str) -> 'Link':
        return Link(text=text_, url=url_)


class CommentBase(SQLModel):
    type: CommentType
    content: str | Link


class Comment(CommentBase, table=True):
    __table_args__ = {'schema': settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    task_id: PK_TYPE = Field(foreign_key='task.id')
    author_id: USER_PK_TYPE = Field(foreign_key='user.id')
    content: str
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )

    author: User = Relationship(sa_relationship_kwargs={"lazy": "joined"})


class CommentRead(CommentBase):
    id: PK_TYPE
    author: UserRead
    created_at: datetime

    @model_validator(mode="after")
    def convert_content(self) -> 'CommentRead':
        """Конвертирует текстовое представления ссылки в объект Link."""
        if self.type == CommentType.LINK:
            self.content = Link.from_str(*self.content.split(SEPARATOR))
        return self


class CommentCreate(CommentBase):
    @model_validator(mode="after")
    def convert_content(self) -> 'CommentCreate':
        """Конвертирует объект Link в текстовое представление."""
        if self.type == CommentType.LINK and isinstance(self.content, Link):
            self.content = self.content.to_str()
        return self

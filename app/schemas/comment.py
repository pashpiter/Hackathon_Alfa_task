# flake8: noqa: VNE003
import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator, ValidationInfo
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, text

from core.config import settings
from schemas.base import PK_TYPE, USER_PK_TYPE
from schemas.user import User, UserRead

# Разделитель, используемый при записи ссылки в БД. В самой БД хранится в виде:
# <текст ссылки><РАЗДЕЛИТЕЛЬ><url ссылки>
SEPARATOR = '$'

WRONG_LINK_CONTENT = ('Для создания комментария типа link, необходимо '
                      'передать объект Link')


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

    @field_validator('content')
    @classmethod
    def convert_content(
            cls,
            content: str | Link,
            validation_info: ValidationInfo
    ) -> str | Link:
        """При необходимости конвертирует текстовое представления ссылки в
        объект Link."""
        if validation_info.data['type'] == CommentType.LINK:
            content = Link.from_str(*content.split(SEPARATOR))
        return content


class CommentCreate(CommentBase):
    @field_validator('content')
    @classmethod
    def convert_content(
            cls,
            content: str | Link,
            validation_info: ValidationInfo
    ) -> str | Link:
        """При необходимости конвертирует объект Link в текстовое
        представление."""
        if validation_info.data['type'] == CommentType.LINK:
            if isinstance(content, str):
                raise ValueError(WRONG_LINK_CONTENT)
            content = content.to_str()
        return content

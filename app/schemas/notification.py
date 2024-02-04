# flake8: noqa: VNE003
import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, text

from core.config import settings
from schemas.base import PK_TYPE, USER_PK_TYPE


class NotificationType(str, enum.Enum):
    SUCCESS = 'success'
    FAIL = 'fail'
    COMMON = 'common'


class NotificationHeader(str, enum.Enum):
    TASK_DONE = "Задача выполнена"
    TASK_NEW = "Новая задача"
    TASK_REVIEW = "Задача на проверке"
    TASK_FAILED = "Задача не выполнена"
    TASK_IN_PROGRESS = "Задача в работе"
    FILE_ATTACHMENT = "Прикреплен файл"
    LINK_ATTACHMENT = "Прикреплена ссылка"
    COMMENT_NEW = "Добавлен комментарий"


class NotificationBase(SQLModel):
    type: NotificationType
    header: str
    content: str
    is_read: bool = False


class Notification(NotificationBase, table=True):
    __table_args__ = {'schema': settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    recipient_id: USER_PK_TYPE
    task_id: PK_TYPE = Field(foreign_key='task.id')
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        ),
    )


class NotificationRead(NotificationBase):
    id: PK_TYPE
    task_id: PK_TYPE
    created_at: datetime

# flake8: noqa: VNE003
import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, text

from core.config import settings
from schemas.base import USER_PK_TYPE, PrimaryKey


class NotificationType(str, enum.Enum):
    SUCCESS = 'success'
    FAIL = 'fail'
    COMMON = 'common'


class NotificationBase(SQLModel):
    pass


class Notification(NotificationBase, PrimaryKey, table=True):
    __table_args__ = {'schema': settings.postgres.schema}

    recipient_id: USER_PK_TYPE
    type: NotificationType
    header: str
    content: str
    is_read: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        ),
    )


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass

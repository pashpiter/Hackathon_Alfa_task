import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, text

from core.config import settings
from schemas.base import PK_TYPE


class TaskStatus(str, enum.Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'
    UNDER_REVIEW = 'under_review'


class TaskBase(SQLModel):
    name: str
    description: str


class Task(TaskBase, table=True):
    __table_args__ = {'schema': settings.postgres.schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.CREATED)
    plan_id: PK_TYPE = Field(default=None, foreign_key='plan.id')
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )
    expires_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True
        )
    )


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: PK_TYPE
    created_at: datetime


class TaskUpdate(TaskBase):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    expires_at: Optional[datetime] = None

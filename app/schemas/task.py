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
    pass


class Task(TaskBase, table=True):
    __table_args__ = {'schema': settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    name: str
    description: str
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
    pass


class TaskUpdate(TaskBase):
    pass

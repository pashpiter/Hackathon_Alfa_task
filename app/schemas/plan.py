import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, text

from core.config import settings
from schemas.base import PK_TYPE, USER_PK_TYPE
from schemas.task import TaskRead


class PlanStatus(str, enum.Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'


class PlanBase(SQLModel):
    aim_description: str
    employee_id: USER_PK_TYPE
    expires_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True
        )
    )


class Plan(PlanBase, table=True):
    __table_args__ = {'schema': settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    status: PlanStatus = Field(default=PlanStatus.CREATED)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )


class PlanCreate(PlanBase):
    pass


class PlanRead(PlanBase):
    id: PK_TYPE
    status: PlanStatus
    created_at: datetime


class PlanReadWithTasks(PlanRead):
    tasks: list[TaskRead] = []


class PlanUpdate(SQLModel):
    aim_description: str

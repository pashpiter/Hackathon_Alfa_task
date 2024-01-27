import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, SQLModel, text

from core.config import settings
from schemas.base import PK_TYPE, USER_PK_TYPE


class PlanStatus(str, enum.Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'


class PlanBase(SQLModel):
    aim_description: str
    employee_id: USER_PK_TYPE


class Plan(PlanBase, table=True):
    __table_args__ = {'schema': settings.postgres.schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    status: PlanStatus = Field(default=PlanStatus.CREATED)
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


class PlanCreate(PlanBase):
    pass


class PlanRead(PlanBase):
    id: PK_TYPE
    status: PlanStatus
    created_at: datetime
    expires_at: datetime


class PlanUpdate(PlanBase):
    aim_description: Optional[str] = None
    status: Optional[PlanStatus] = None
    expires_at: Optional[datetime] = None

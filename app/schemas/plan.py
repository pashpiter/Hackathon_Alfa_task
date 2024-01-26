from sqlmodel import SQLModel, Field, text, DateTime, Column
from typing import Optional
from datetime import datetime
import enum
from core.config import settings
from schemas.base import USER_PK_TYPE, PrimaryKey


class PlanStatus(str, enum.Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'


class PlanBase(SQLModel):
    pass


class Plan(PlanBase, PrimaryKey, table=True):
    __table_args__ = {'schema': settings.postgres.schema}

    aim_description: str
    status: PlanStatus
    employee_id: USER_PK_TYPE
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
    pass


class PlanUpdate(PlanBase):
    pass

# flake8: noqa: VNE003
from datetime import date
from dateutil.relativedelta import relativedelta
import enum
from typing import List, Optional

from sqlmodel import Column, Date, Field, Relationship, SQLModel, text

from core.config import settings
from core.utils import date_today
from schemas.base import EXPIRES_DATE_TYPE, PK_TYPE, USER_PK_TYPE
from schemas.task import Task, TaskRead
from schemas.user import User, UserRead


class PlanStatus(str, enum.Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'


class PlanBase(SQLModel):
    aim_description: str
    expires_at: Optional[date] = Field(
        sa_column=Column(
            Date,
            nullable=False
        )
    )


class Plan(PlanBase, table=True):
    __table_args__ = {"schema": settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    employee_id: USER_PK_TYPE = Field(foreign_key='user.id')
    status: PlanStatus = Field(default=PlanStatus.CREATED)
    created_at: Optional[date] = Field(
        sa_column=Column(
            Date,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )

    tasks: List["Task"] = Relationship(
        back_populates="plan",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "lazy": "joined"
        }
    )
    employee: User = Relationship(sa_relationship_kwargs={"lazy": "joined"})


class PlanCreate(PlanBase):
    employee_id: int
    expires_at: Optional[EXPIRES_DATE_TYPE] = \
        date_today() + relativedelta(months=6)


class PlanRead(PlanBase):
    id: PK_TYPE
    status: PlanStatus
    created_at: date
    employee: UserRead


class PlanReadWithTasks(PlanRead):
    tasks: List[TaskRead] | None = []


class PlanUpdate(SQLModel):
    aim_description: Optional[str] = None
    expires_at: Optional[EXPIRES_DATE_TYPE] = None

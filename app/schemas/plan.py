from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import enum
from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Column, Date, Field, Relationship, SQLModel, text

from core.config import settings
from core.utils import date_today
from schemas.base import PK_TYPE, USER_PK_TYPE
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
            nullable=True
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
    employee: User = Relationship(
        back_populates="plan",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "lazy": "joined"
        }
    )


class PlanCreate(PlanBase):
    employee_id: int
    expires_at: Optional[date] = date_today() + relativedelta(months=6)

    @field_validator("expires_at", mode="before")
    def validate_date(cls, d: object) -> object:
        if isinstance(d, str):
            d = datetime.strptime(d, "%d.%m.%Y").date()
        if d < date_today():
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Нельзя установить дату в прошлом"
            )
        elif d - date_today() < timedelta(days=1):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Дата окончания не может быть меньше одного дня"
            )
        return d


class PlanRead(PlanBase):
    id: PK_TYPE
    status: PlanStatus
    created_at: date
    employee: UserRead


class PlanReadWithTasks(PlanRead):
    tasks: List[TaskRead] = []


class PlanUpdate(SQLModel):
    aim_description: str

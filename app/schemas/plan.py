import enum
from datetime import datetime, timedelta, date
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Column, Date, Field, Relationship, SQLModel, text

from core.config import settings
from core.utils import date_today
from schemas.base import PK_TYPE, USER_PK_TYPE
from schemas.task import Task, TaskRead
from schemas.user import User


class PlanStatus(str, enum.Enum):
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'


class PlanBase(SQLModel):
    aim_description: str
    employee_id: USER_PK_TYPE = Field(foreign_key="user.id")
    expires_at: Optional[date] = Field(
        sa_column=Column(
            Date,
            nullable=True
        )
    )


class Plan(PlanBase, table=True):
    __table_args__ = {"schema": settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    status: PlanStatus = Field(default=PlanStatus.CREATED)
    created_at: Optional[date] = Field(
        sa_column=Column(
            Date,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )

    tasks: list["Task"] = Relationship(
        back_populates="plan",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "lazy": "joined"
        }
    )
    employee: Optional[User] = Relationship(
        back_populates="plan",
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "lazy": "joined"
        }
    )


class PlanCreate(PlanBase):
    created_at: date

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
    employee_id: User
    status: PlanStatus
    created_at: date


class PlanReadWithTasks(PlanRead):
    tasks: list[TaskRead] = []


class PlanUpdate(SQLModel):
    aim_description: str

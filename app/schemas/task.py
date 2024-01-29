import enum
from datetime import datetime, timedelta, date
from http import HTTPStatus
from typing import List, Optional, TYPE_CHECKING

from core.config import settings
from core.utils import date_today
from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Column, Date, Field, Relationship, SQLModel, text

from schemas.base import PK_TYPE
from schemas.comment import CommentRead, Comment
if TYPE_CHECKING:
    from schemas.plan import Plan


class TaskStatus(str, enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"
    UNDER_REVIEW = "under_review"


class TaskBase(SQLModel):
    name: str
    description: str
    status: TaskStatus = Field(default=TaskStatus.CREATED)
    created_at: Optional[date] = Field(
        sa_column=Column(
            Date,
            nullable=False,
            server_default=text('TIMEZONE("utc", now())')
        )
    )
    expires_at: Optional[date] = Field(
        sa_column=Column(
            Date,
            nullable=True
        )
    )


class Task(TaskBase, table=True):
    __table_args__ = {"schema": settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    plan_id: PK_TYPE = Field(foreign_key="plan.id")

    comments: Comment = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete", "lazy": "joined"}
    )
    plan: Optional["Plan"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    created_at: Optional[date] = date_today()

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


class TaskRead(TaskBase):
    id: PK_TYPE


class TaskReadWithComments(TaskRead):
    comments: List[CommentRead] | None = []


class TaskUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    expires_at: Optional[date] = None

    @field_validator("expires_at", mode="before")
    def validate_date(cls, d: object) -> object:
        if d is None:
            return
        if isinstance(d, str):
            d = datetime.strptime(d, "%d.%m.%Y").date()
        return d

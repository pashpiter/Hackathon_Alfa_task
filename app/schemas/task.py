import enum
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List, Optional

from core.config import settings
from core.utils import date_now
from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel, text

from schemas.base import PK_TYPE
from schemas.comment import CommentRead


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
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text('TIMEZONE("utc", now())')
        )
    )
    expires_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True
        )
    )


class Task(TaskBase, table=True):
    __table_args__ = {"schema": settings.postgres.db_schema}

    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)
    plan_id: PK_TYPE = Field(default=None, foreign_key="plan.id")

    # comments: List["Comment"] = Relationship(
    #     back_populates="comment",
    #     sa_relationship_kwargs={"cascade": "delete"})
        # Doesn"t work vvv
        # sa_relationship_kwargs={"cascade": "all, delete"})


class TaskCreate(TaskBase):
    created_at: Optional[datetime] = date_now()

    @field_validator("expires_at", mode="before")
    def validate_date(cls, d: object) -> object:
        if isinstance(d, str):
            d = datetime.strptime(d, "%d.%m.%Y").date()
        if d - date_now() < timedelta(days=1):
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Дата окончания не может быть меньше одного дня"
            )
        return d


class TaskRead(TaskBase):
    id: int


class TaskReadWithComments(TaskRead):
    comments: List[CommentRead] = []


class TaskUpdate(SQLModel):
    name: str = None
    description: str = None
    status: Optional[TaskStatus] = None

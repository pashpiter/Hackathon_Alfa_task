# flake8: noqa: VNE003
import enum
from datetime import date
from typing import List, Optional, TYPE_CHECKING

from core.config import settings
from core.utils import date_today
from pydantic import model_validator
from sqlmodel import Column, Date, Field, Relationship, SQLModel, text

from schemas.base import PK_TYPE, EXPIRES_DATE_TYPE
from schemas.comment import CommentRead

if TYPE_CHECKING:
    from schemas.comment import Comment
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

    comments: List["Comment"] = Relationship(
        sa_relationship_kwargs={
            "cascade": "all, delete",
            "lazy": "joined"
        }
    )
    plan: Optional["Plan"] = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={
            "lazy": "joined"
        }
    )


class TaskCreate(TaskBase):
    created_at: Optional[date] = date_today()
    expires_at: Optional[EXPIRES_DATE_TYPE] = None


class TaskRead(TaskBase):
    id: PK_TYPE

    @model_validator(mode="before")
    def editing_expires_at(cls, data: Task) -> Task:
        """Добавление даты дедлайна из Плана, если дедлайна у задачи нет"""
        if isinstance(data, Task) and not data.expires_at:
            data.expires_at = data.plan.expires_at
        return data


class TaskReadWithComments(TaskRead):
    comments: List[CommentRead] | None = []


class TaskUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    expires_at: Optional[EXPIRES_DATE_TYPE] = None

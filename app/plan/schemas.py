# Используйте SQLModel!!!!!  https://sqlmodel.tiangolo.com/tutorial/fastapi/
# ПРИМЕР https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/
from sqlmodel import SQLModel, Field, text, DateTime, Column
from typing import Optional
from datetime import datetime


PK_TYPE = int
USER_PK_TYPE = int


class PrimaryKey:
    """Класс для добавления id(pk) к схемам"""
    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)


class UserBase(SQLModel):
    pass


class User(UserBase, PrimaryKey, table=True):
    pass


class UserRead(UserBase):
    pass


class SupervisorEmployee(SQLModel, PrimaryKey, table=True):
    pass


# *****************************************************************************


class PlanBase(SQLModel):
    pass


class Plan(PlanBase, PrimaryKey, table=True):
    name: str
    status: str  # TODO: добавить Enum
    employee_id: USER_PK_TYPE
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )
    expired_at: Optional[datetime] = Field(
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


# *****************************************************************************


class TaskBase(SQLModel):
    pass


class Task(TaskBase, PrimaryKey, table=True):
    aim_description: str
    status: str  # TODO: добавить Enum
    plan_id: PK_TYPE = Field(default=None, foreign_key='plan.id')
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )
    expired_at: Optional[datetime] = Field(
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


# *****************************************************************************


class CommentBase(SQLModel):
    pass


class Comment(CommentBase, PrimaryKey, table=True):
    task_id: PK_TYPE = Field(default=None, foreign_key='task.id')
    author_id: USER_PK_TYPE
    type: str  # TODO: добавить Enum
    content: str
    is_read: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )


class CommentRead(CommentBase):
    pass


class CommentCreate(CommentBase):
    pass


# *****************************************************************************


class NotificationBase(SQLModel):
    pass


class Notification(NotificationBase, PrimaryKey, table=True):
    recipient_id: USER_PK_TYPE
    type: str  # TODO: добавить Enum
    header: str
    content: str
    is_read: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        )
    )


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass

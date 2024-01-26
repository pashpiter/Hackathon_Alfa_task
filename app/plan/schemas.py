from sqlmodel import SQLModel, Field, text, DateTime, Column
from typing import Optional
from datetime import datetime
import enum

PK_TYPE = int
USER_PK_TYPE = int


class StatusBase:
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'


class PrimaryKey:
    """Класс для добавления id(pk) к схемам"""
    id: Optional[PK_TYPE] = Field(default=None, primary_key=True)


# *****************************************************************************


class UserBase(SQLModel):
    full_name: str
    position: str


class User(UserBase, PrimaryKey, table=True):
    token: str
    supervisor_id: Optional[int]


class UserRead(UserBase):
    pass


# *****************************************************************************

class PlanStatus(StatusBase, str, enum.Enum):
    pass


class PlanBase(SQLModel):
    pass


class Plan(PlanBase, PrimaryKey, table=True):
    aim_description: str
    status: str = Field(sa_column_kwargs={'info': {'choices': PlanStatus}})
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


# *****************************************************************************


class TaskStatus(StatusBase, str, enum.Enum):
    UNDER_REVIEW = 'under_review'


class TaskBase(SQLModel):
    pass


class Task(TaskBase, PrimaryKey, table=True):
    name: str
    description: str
    status: str = Field(sa_column_kwargs={'info': {'choices': TaskStatus}})
    plan_id: PK_TYPE = Field(default=None, foreign_key='plan.id')
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


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


# *****************************************************************************


class CommentType(str, enum.Enum):
    TEXT = 'text'
    FILE = 'file'
    LINK = 'link'


class CommentBase(SQLModel):
    pass


class Comment(CommentBase, PrimaryKey, table=True):
    task_id: PK_TYPE = Field(default=None, foreign_key='task.id')
    author_id: USER_PK_TYPE
    type: str = Field(sa_column_kwargs={'info': {'choices': CommentType}})
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


class NotificationType(str, enum.Enum):
    SUCCESS = 'success'
    FAIL = 'fail'
    COMMON = 'common'


class NotificationBase(SQLModel):
    pass


class Notification(NotificationBase, PrimaryKey, table=True):
    recipient_id: USER_PK_TYPE
    type: str  # TODO: добавить Enum
    header: str
    text: str
    is_read: bool = Field(default=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=False,
            server_default=text("TIMEZONE('utc', now())")
        ),
    )


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    pass

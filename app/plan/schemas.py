# Используйте SQLModel!!!!!  https://sqlmodel.tiangolo.com/tutorial/fastapi/
# ПРИМЕР https://sqlmodel.tiangolo.com/tutorial/fastapi/session-with-dependency/
from sqlmodel import SQLModel, Field
from typing import Optional


class PrimaryKey(SQLModel):
    """Класс для добавления id(pk) к схемам"""
    id: Optional[int] = Field(default=None, primary_key=True)


class UserBase(SQLModel):
    full_name: str
    position: str


class User(UserBase, PrimaryKey, table=True):
    token: str
    supervisor_id: Optional[int]


class UserRead(UserBase):
    id: int


class PlanBase(SQLModel):
    pass


class Plan(PlanBase, PrimaryKey, table=True):
    pass


class PlanCreate(PlanBase):
    pass


class PlanRead(PlanBase):
    pass


class PlanUpdate(SQLModel):
    # Взять поля из плана, которые можно менять
    pass


class TaskBase(SQLModel):
    pass


class Task(TaskBase, PrimaryKey):
    pass


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    pass


class TaskUpdate(SQLModel):
    # Взять поля из задачи, которые можно менять
    pass


class CommentBase(SQLModel):
    pass


class Comment(CommentBase, PrimaryKey, table=True):
    pass


class CommentRead(CommentBase):
    pass


class CommentCreate(CommentBase):
    pass


class AttachmentBase(SQLModel):
    pass


class Attachment(AttachmentBase, PrimaryKey, table=True):
    pass


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentRead(AttachmentBase):
    pass

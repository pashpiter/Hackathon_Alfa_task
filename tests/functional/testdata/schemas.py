import enum
from pydantic import BaseModel

PK_TYPE = int
USER_PK_TYPE = int


class User(BaseModel):
    id: USER_PK_TYPE = None
    full_name: str = None
    position: str = None
    token: str = None
    supervisor_id: USER_PK_TYPE | None = None
    photo: str | None = None


class NotificationType(str, enum.Enum):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'
    COMMON = 'COMMON'


class PlanStatus(str, enum.Enum):
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    FAILED = 'FAILED'


class TaskStatus(str, enum.Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"
    UNDER_REVIEW = "UNDER_REVIEW"

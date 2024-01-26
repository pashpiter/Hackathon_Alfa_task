from core.logger import logger_factory
from db.crud.base import CRUDBase
from schemas import Task


class CRUDTask(CRUDBase):
    pass


task_crud = CRUDTask(Task, logger_factory(__name__))

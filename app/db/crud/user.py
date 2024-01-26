from core.logger import logger_factory
from db.crud.base import CRUDBase
from plan.schemas import User


class CRUDUser(CRUDBase):
    pass


user_crud = CRUDUser(User, logger_factory(__name__))

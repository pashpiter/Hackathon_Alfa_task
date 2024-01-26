from core.logger import logger_factory
from db.crud.base import CRUDBase
from plan.schemas import Comment


class CRUDComment(CRUDBase):
    pass


comment_crud = CRUDComment(Comment, logger_factory(__name__))

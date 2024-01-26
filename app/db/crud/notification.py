from core.logger import logger_factory
from db.crud.base import CRUDBase
from plan.schemas import Notification


class CRUDNotification(CRUDBase):
    pass


notification_crud = CRUDNotification(Notification, logger_factory(__name__))

from core.logger import logger_factory
from db.crud.base import CRUDBase
from plan.schemas import Plan


class CRUDPlan(CRUDBase):
    pass


plan_crud = CRUDPlan(Plan, logger_factory(__name__))

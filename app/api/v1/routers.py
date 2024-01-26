from fastapi import APIRouter

from api.v1.endpoints import (comment_router, notification_router, plan_router,
                              task_router)

v1_router = APIRouter(prefix='/api/v1')

v1_router.include_router(plan_router, tags=['Plans'])
v1_router.include_router(task_router, tags=['Tasks'])
v1_router.include_router(comment_router, tags=['Comments'])
v1_router.include_router(notification_router, tags=['Notifications'])

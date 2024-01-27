from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.routers import v1_router
from core.config import settings

app = FastAPI(
    title=settings.app.name,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(v1_router)

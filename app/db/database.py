from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from core.config import settings

SQLModel.metadata.schema = settings.postgres.db_schema
DATABASE_URL = settings.postgres.database_url

async_engine = create_async_engine(DATABASE_URL, echo=settings.app.debug)

async_session_factory = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncSession:
    """
    Асинхронный генератор сессий.
    Целесообразность его использования в проекте под вопросом.
    Пока предлагаю использовать, как рабочую версию.

    Рекомендуется вызывать сессию через зависимости:

    from fastapi import Depends
    from db.database import get_async_func

    async func(session = Depends(get_async_session)):
        ...
        session.exec(query | statement)
    """
    async with async_session_factory() as session:
        yield session

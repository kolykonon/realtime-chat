from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from chat_service.core.config import get_settings

settings = get_settings()
engine = create_async_engine(str(settings.postgres_settings.postgres_dsn))
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session

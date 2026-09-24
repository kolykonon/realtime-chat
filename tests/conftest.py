import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.chat_service.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app)) as client:
        yield client

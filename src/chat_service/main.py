from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from chat_service.db.base import Base
from chat_service.db.dep import engine
from chat_service.core.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.security_settings.secret_key,
    https_only=True,
    same_site='lax'
)


@app.get('/health')
def health() -> dict[str,str]:
    return {'status': 'healthy'}

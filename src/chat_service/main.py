from fastapi import FastAPI
from chat_service.db.base import Base
from chat_service.db.dep import engine

async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

app = FastAPI(lifespan=lifespan)

@app.get('/health')
def health() -> dict[str,str]:
    return {'status': 'healthy'}

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from chat_service.api.v1 import router as v1_router
from chat_service.core.config import get_settings

settings = get_settings()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_router, prefix=settings.api_v1_prefix)



@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}

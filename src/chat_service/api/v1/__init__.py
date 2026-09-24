from fastapi import APIRouter

from chat_service.api.v1.auth import router as auth_router
from chat_service.api.v1.user import router as user_router

router = APIRouter()

router.include_router(user_router)
router.include_router(auth_router)

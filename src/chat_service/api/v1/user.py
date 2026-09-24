from fastapi import APIRouter, HTTPException, status

from chat_service.api.deps import CurrentUserDep
from chat_service.schemas.user import UserCreate
from chat_service.services.user_service import UserServiceDep

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=None)
async def register_user(data: UserCreate, service: UserServiceDep):
    try:
        await service.create(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me")
async def get_me(user: CurrentUserDep):
    return {"username": user.username}

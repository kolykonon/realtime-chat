from fastapi import Depends, HTTPException,status

from chat_service.schemas.user import UserCreate
from chat_service.services.user_service import get_user_service, UserService
from chat_service.core.security import hash_password


class AuthService:
    def __init__(self, user_service: UserService = Depends(get_user_service)) -> None:
        self.user_service = user_service

    async def register_user(self,user: UserCreate) -> None:
        existed = await self.user_service.get_user(user.username)
        if existed is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        user.password = hash_password(user.password)
        await self.user_service.create_user(user)

def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    return AuthService(user_service)



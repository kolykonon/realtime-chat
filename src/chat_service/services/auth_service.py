from typing import Annotated

from fastapi import Depends

from chat_service.core.security import dummy_hash, verify_password
from chat_service.services.user_service import UserService, UserServiceDep


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def authenticate_user(self, username: str, password: str):
        user = await self.user_service.get_user_by_username(username)
        if not user:
            verify_password(password, dummy_hash)
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

def get_auth_service(user_service: UserServiceDep) -> AuthService:
    return AuthService(user_service)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

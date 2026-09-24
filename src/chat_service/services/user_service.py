from typing import Annotated

from fastapi import Depends

from chat_service.core.security import hash_password
from chat_service.db.models import User
from chat_service.db.repositories.user_repo import UserRepo, UserRepoDep
from chat_service.schemas.user import UserCreate, UserCreateDB, UserRead, UserUpdate
from chat_service.services.base_service import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate, UserRead, UserRepo]):
    def __init__(self, repo: UserRepo):
        super().__init__(repo)

    async def create(self, data: UserCreate) -> UserRead:
        existed = await self.repo.get_by_username(data.username)
        if existed:
            raise ValueError("Username already exists")
        user = await self.repo.create(
            UserCreateDB(username=data.username, hashed_password=hash_password(data.password))
        )
        return UserRead.model_validate(user)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.repo.get_by_username(username)


def get_user_service(repo: UserRepoDep) -> UserService:
    return UserService(repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

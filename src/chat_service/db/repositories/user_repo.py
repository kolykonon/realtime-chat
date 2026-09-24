from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from chat_service.db.dep import SessionDep
from chat_service.db.models.user import User
from chat_service.db.repositories.base_repo import BaseRepo
from chat_service.schemas.user import UserCreateDB, UserUpdate


class UserRepo(BaseRepo[User,UserCreateDB,UserUpdate]):
    def __init__(self, session: SessionDep) -> None:
        super().__init__(session, User)

    async def get_by_username(self,username: str) -> User | None:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

def get_user_repo(session: SessionDep) -> UserRepo:
    return UserRepo(session)

UserRepoDep = Annotated[UserRepo, Depends(get_user_repo)]

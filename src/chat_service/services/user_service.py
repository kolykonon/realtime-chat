from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from chat_service.db.dep import get_db
from chat_service.db.models.user import User
from chat_service.schemas.user import UserCreate


class UserService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    async def get_user(self, username: str, db: Session = Depends(get_db)) -> Optional[User]:
        query = select(User).where(User.username == username)
        user = await self.session.execute(query).scalar_one_or_none()
        return user | None

    async def create_user(self, user: UserCreate, session: Session = Depends(get_db)):
        self.session.add(user)
        self.session.commit()
        return user


def get_user_service(session: Session = Depends(get_db)):
    return UserService(session)


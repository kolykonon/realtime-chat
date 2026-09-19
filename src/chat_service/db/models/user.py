from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from chat_service.db.base import Base
from chat_service.db.mixins.id_mixin import IDMixin
from chat_service.db.mixins.timestamp_mixin import TimestampMixin



class User(Base,IDMixin,TimestampMixin):
    __tablename__ = 'users'
    username: Mapped[str] = mapped_column(String(100), nullable=False,unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    class Config:
        orm_mode = True



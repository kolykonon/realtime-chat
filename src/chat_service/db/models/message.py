from sqlalchemy import Integer, ForeignKey, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from chat_service.db.base import Base
from chat_service.db.mixins.id_mixin import IDMixin
from chat_service.db.mixins.timestamp_mixin import TimestampMixin


class Message(Base, IDMixin, TimestampMixin):
    __tablename__ = 'messages'
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    text = mapped_column(Text, nullable=False)

    class Config:
        orm_mode = True


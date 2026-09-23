from collections.abc import Sequence
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy import select

from chat_service.db.base import Base
from chat_service.db.dep import SessionDep

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseRepo[ModelType: Base, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel, ResponseSchemaType: BaseModel]:
    def __init__(self, session: SessionDep,model: type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def get_list(self,
        limit: int | None = None,
        offset: int | None = None
    ) -> Sequence[ModelType]:
        query = select(self.model)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one(self, id: int) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)  # type: ignore[attr-defined] ругается пайрайт, хотя работает
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, create_schema: CreateSchemaType) -> None:
        obj = self.model(**create_schema.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.flush()

    async def update(self, obj: ModelType, update_schema: UpdateSchemaType) -> None:
        for attribute, value in update_schema.model_dump(exclude_unset=True).items():
            setattr(obj,attribute, value)
        await self.session.flush()

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.commit()
        await self.session.flush()


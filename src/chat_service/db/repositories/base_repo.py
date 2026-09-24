from collections.abc import Sequence

from pydantic import BaseModel
from sqlalchemy import select

from chat_service.db.base import Base
from chat_service.db.dep import SessionDep


class BaseRepo[ModelType: Base, CreateSchemaType: BaseModel, UpdateSchemaType: BaseModel]:
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
        return await self.session.get(self.model, id)

    async def create(self, create_schema: CreateSchemaType) -> ModelType:
        obj = self.model(**create_schema.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.flush()
        return obj

    async def update(self, obj: ModelType, update_schema: UpdateSchemaType) -> None:
        for attribute, value in update_schema.model_dump(exclude_unset=True).items():
            setattr(obj,attribute, value)
        await self.session.flush()

    async def delete(self, obj: ModelType) -> None:
        await self.session.delete(obj)
        await self.session.commit()
        await self.session.flush()

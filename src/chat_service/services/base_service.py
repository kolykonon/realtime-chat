from collections.abc import Sequence

from pydantic import BaseModel

from chat_service.db.repositories.base_repo import BaseRepo


class BaseService[
    ModelType,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
    ResponseSchemaType: BaseModel,
    RepoType: BaseRepo,
]:
    def __init__(self, repo: RepoType, response_schema: type[ResponseSchemaType]):
        self.repo = repo
        self.response_schema = response_schema

    async def create(self, data: CreateSchemaType) -> ResponseSchemaType:
        new_obj = await self.repo.create(data)
        return self.response_schema.model_validate(new_obj)

    async def update(self, id: int, data: UpdateSchemaType) -> ResponseSchemaType:
        obj = await self.repo.get_one(id)
        if obj is None:
            raise ValueError(f"Object with id {id} not found")
        await self.repo.update(obj, data)
        return self.response_schema.model_validate(obj)

    async def get(self, id: int) -> ModelType | None:
        return await self.repo.get_one(id)

    async def get_list(self, offset: int, limit: int) -> Sequence[ModelType]:
        return await self.repo.get_list(offset, limit)

    async def delete(self, id: int) -> None:
        obj = await self.repo.get_one(id)
        if obj is None:
            raise ValueError(f"Object with id {id} not found")
        await self.repo.delete(obj)

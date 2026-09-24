from collections.abc import AsyncIterator

from redis.asyncio import Redis

redis_client: Redis = Redis.from_url("redis://localhost:6379")


async def get_redis() -> AsyncIterator[Redis]:
    yield redis_client

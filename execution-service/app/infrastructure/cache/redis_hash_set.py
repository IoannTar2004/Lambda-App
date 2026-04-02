from typing import Any

import redis.asyncio as redis_asyncio
from application.ports.cache_hash_set import CacheHashSet


class RedisHashSet(CacheHashSet):

    def __init__(self, client: redis_asyncio.Redis):
        self.client = client

    async def add(self, key: str, *value: Any) -> None:
        await self.client.sadd(key, *value)

    async def get(self, key: str) -> Any:
        return await self.client.smembers(key)

    async def contains(self, key: str, value: Any) -> bool:
        return bool(await self.client.sismember(key, value))

    async def remove(self, key: str, *value: str) -> None:
        await self.client.srem(key, *value)

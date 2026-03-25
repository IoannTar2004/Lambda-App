import redis.asyncio as redis_asyncio

from application.ports.cache import Cache


class RedisClient(Cache):

    def __init__(self, client: redis_asyncio.Redis):
        self.client = client

    async def zadd(self, key: str, value: dict) -> None:
        await self.client.zadd(key, value)

    async def zrange(self, key: str, start: int = 0, stop: int = -1, desc=False) -> list:
        return await self.client.zrange(key, start, stop, desc)

    async def zrem(self, key: str, entry_key: str) -> None:
        await self.client.zrem(key, entry_key)

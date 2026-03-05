import redis.asyncio as redis

from application.ports.cache import Cache


class RedisClient(Cache):

    def __init__(self, client: redis.Redis):
        self.client = client

    async def set(self, key: str, value) -> None:
        await self.client.set(key, value)

    async def get(self, key: str) -> str:
        res = await self.client.get(key)
        return res
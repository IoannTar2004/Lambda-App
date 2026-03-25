import redis.asyncio as redis_asyncio

from application.ports.log_stream import LogStream


class RedisLogStream(LogStream):

    def __init__(self, client: redis_asyncio.Redis):
        self.client = client

    async def add(self, key: str, value: dict) -> str:
        return await self.client.xadd(key, value)

    async def read(self, key: str, begin: str = "-", end: str = "+", count=500) -> dict:
        return await self.client.xrange(key, begin, end, count)

    async def delete(self, key: str):
        await self.client.delete(key)
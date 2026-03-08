from application.ports.cache import Cache


class RedisClient(Cache):

    def __init__(self, client):
        self.client = client

    async def set(self, key: str, value, ex=300) -> None:
        await self.client.set(key, value, ex=ex)

    async def get(self, key: str) -> str:
        res = await self.client.get(key)
        return res

    async def delete(self, key: str) -> None:
        await self.client.delete(key)
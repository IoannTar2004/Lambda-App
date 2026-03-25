import redis.asyncio as redis_asyncio


class Redis:

    def __init__(self):
        self.redis = None

    async def start(self, host: str, port: int):
        self.redis = redis_asyncio.Redis(host=host, port=port, decode_responses=True)

    async def close(self):
        await self.redis.close()

redis_connection = Redis()
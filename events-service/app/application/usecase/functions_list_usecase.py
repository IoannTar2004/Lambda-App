from application.ports.async_request import AsyncRequest
from application.ports.cache import Cache


class FunctionsListUseCase:

    def __init__(self, cache: Cache, async_req: AsyncRequest):
        self.cache = cache
        self.async_req = async_req

    async def execute(self, filename: str) -> list[str]:
        # res = await self.cache.get(filename)
        res = await self.async_req.get("http://localhost:8001/api/code/listdir", {"path": filename})
        return res
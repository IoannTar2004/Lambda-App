import httpx

from application.ports.async_request import AsyncRequest


class HttpxAsyncRequest(AsyncRequest):

    async def get(self, url: str, params: dict) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return response.json()
from typing import AsyncGenerator, Any

import httpx

from application.ports.async_request import AsyncRequest
from infrastructure.config.consul import get_service_url


class HttpxAsyncRequest(AsyncRequest):

    async def get(self, endpoint: str | None, service_name: str | None, params: dict) -> dict:
        url = await get_service_url(service_name) + endpoint

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_stream(self, endpoint: str | None, service_name: str | None, params: dict, chunk_size: int = 1024 *1024)\
            -> AsyncGenerator[Any, Any]:
        url = await get_service_url(service_name) + endpoint

        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url, params=params) as response:
                response.raise_for_status()
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    yield chunk
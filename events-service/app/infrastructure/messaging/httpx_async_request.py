from typing import AsyncGenerator, Any

import httpx

from application.ports.async_request import AsyncRequest
from infrastructure.config.consul import get_service_url

class HttpxAsyncRequest(AsyncRequest):

    async def get(self, endpoint: str | None, service_name: str | None, params: dict, headers = None) -> dict:
        url = await get_service_url(service_name) + endpoint

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            self._print_error(e)
            raise e

    async def get_stream(self, endpoint: str | None, service_name: str | None, params: dict, chunk_size: int = 1024 *1024,
                         headers = None) \
            -> AsyncGenerator[Any, Any]:
        url = await get_service_url(service_name) + endpoint

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("GET", url, params=params, headers=headers) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                        yield chunk
        except httpx.HTTPStatusError as e:
            self._print_error(e)
            raise e

    async def post(self, endpoint: str | None, service_name: str | None, json: dict = None,
                   data: dict = None, files: dict = None, headers = None) -> Any:
        url = await get_service_url(service_name) + endpoint
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=json, data=data, files=files, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            self._print_error(e)
            raise e

    async def delete(self, endpoint: str | None, service_name: str | None, json: dict = None, params: dict = None,
                     headers = None) -> Any:
        url = await get_service_url(service_name) + endpoint
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request("DELETE", url, json=json, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            self._print_error(e)
            raise e


    def _print_error(self, e):
        print(f"Status code: {e.response.status_code}")
        print(f"Response text: {e.response.text}")
        print(f"Response headers: {e.response.headers}")
        print(f"Request URL: {e.request.url}")
        print(f"Request method: {e.request.method}")
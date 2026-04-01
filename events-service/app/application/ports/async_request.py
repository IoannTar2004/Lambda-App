from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any


class AsyncRequest(ABC):

    @abstractmethod
    async def get(self, endpoint: str | None, service_name: str | None, params: dict, headers = None) -> Any:
        pass

    @abstractmethod
    async def get_stream(self, endpoint: str | None, service_name: str | None, params: dict, chunk_size: int = 1024*1024,
                         headers = None)\
            -> AsyncGenerator[Any, Any]:
        pass

    @abstractmethod
    async def post(self, endpoint: str | None, service_name: str | None, json: dict = None,
                   data: dict = None, files: dict = None, headers = None) -> Any:
        pass

    @abstractmethod
    async def delete(self, endpoint: str | None, service_name: str | None, json: dict, headers = None) -> Any:
        pass
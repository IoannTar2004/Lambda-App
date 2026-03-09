from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any


class AsyncRequest(ABC):

    @abstractmethod
    async def get(self, endpoint: str | None, service_name: str | None, params: dict) -> Any:
        pass

    @abstractmethod
    async def get_stream(self, endpoint: str | None, service_name: str | None, params: dict, chunk_size: int = 1024*1024)\
            -> AsyncGenerator[Any, Any]:
        pass

    @abstractmethod
    async def post(self, endpoint: str | None, service_name: str | None, params: dict) -> Any:
        pass

    @abstractmethod
    async def delete(self, endpoint: str | None, service_name: str | None, params: dict) -> Any:
        pass
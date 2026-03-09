from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any


class AsyncStorage(ABC):

    @abstractmethod
    async def upload(self, bucket: str | None, path: str, data: bytes) -> None:
        pass

    @abstractmethod
    async def download(self, bucket: str | None, path: str) -> AsyncGenerator[bytes, Any]:
        pass

    @abstractmethod
    async def remove(self, bucket: str | None, path: str) -> None:
        pass

    @abstractmethod
    async def exists(self, bucket: str | None, path: str) -> bool:
        pass

    @abstractmethod
    async def listdir(self, bucket: str | None, path: str) -> tuple[list[Any], list[Any]]:
        pass

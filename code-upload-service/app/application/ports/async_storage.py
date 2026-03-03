from abc import ABC, abstractmethod
from typing import BinaryIO, AsyncGenerator, Any


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

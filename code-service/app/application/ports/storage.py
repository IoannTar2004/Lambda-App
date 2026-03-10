from abc import ABC, abstractmethod
from typing import AsyncGenerator, Any


class Storage(ABC):

    @abstractmethod
    async def upload(self, bucket: str | None, path: str, data: bytes) -> None:
        pass

    @abstractmethod
    async def download(self, bucket: str | None, path: str) -> AsyncGenerator[bytes, Any]:
        pass

    @abstractmethod
    async def delete(self, bucket: str | None, path: str) -> None:
        pass

    @abstractmethod
    async def delete_objects(self, bucket: str | None, list_object: list) -> None:
        pass

    @abstractmethod
    async def exists(self, bucket: str | None, path: str) -> bool:
        pass

    @abstractmethod
    async def listdir(self, bucket: str | None, path: str) -> tuple[list[Any], list[Any]]:
        pass

    @abstractmethod
    async def recursive_listdir(self, bucket: str | None, path: str) -> list[str]:
        pass

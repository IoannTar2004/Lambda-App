from abc import ABC, abstractmethod


class Cache(ABC):

    @abstractmethod
    async def set(self, key: str, value, ex=300) -> None:
        pass

    @abstractmethod
    async def get(self, key: str) -> str:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
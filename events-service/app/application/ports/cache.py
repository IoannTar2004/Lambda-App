from abc import ABC, abstractmethod


class Cache(ABC):

    @abstractmethod
    async def set(self, key: str, value) -> None:
        pass

    @abstractmethod
    async def get(self, key: str) -> str:
        pass
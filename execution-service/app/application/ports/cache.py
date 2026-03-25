from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):

    @abstractmethod
    async def zadd(self, key: str, value: dict) -> None:
        pass

    @abstractmethod
    async def zrange(self, key: str, start: int = 0, stop: int = -1, desc=False) -> list:
        pass

    @abstractmethod
    async def zrem(self, key: str, entry_key: str) -> None:
        pass
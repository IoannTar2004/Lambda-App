from abc import ABC, abstractmethod
from typing import Any


class CacheHashSet(ABC):

    @abstractmethod
    async def add(self, key: str, *values: Any) -> None:
        pass

    @abstractmethod
    async def get(self, key: str) -> Any:
        pass

    @abstractmethod
    async def contains(self, key: str, value: Any) -> bool:
        pass

    @abstractmethod
    async def remove(self, key: str, *values: Any) -> None:
        pass

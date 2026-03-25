from abc import ABC, abstractmethod


class LogStream(ABC):

    @abstractmethod
    async def add(self, key: str, value: dict) -> str:
        pass

    @abstractmethod
    async def read(self, key: str, begin: str = "-", end: str = "+", count=500) -> dict:
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass
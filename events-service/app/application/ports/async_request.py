from abc import ABC, abstractmethod


class AsyncRequest(ABC):

    @abstractmethod
    async def get(self, url: str, params: dict) -> dict:
        pass
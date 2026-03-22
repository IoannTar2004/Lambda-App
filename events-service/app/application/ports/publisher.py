from abc import ABC, abstractmethod


class Publisher(ABC):

    @abstractmethod
    async def publish(self, message, topic: str):
        pass
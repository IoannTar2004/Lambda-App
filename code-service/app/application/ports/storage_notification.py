from abc import ABC, abstractmethod


class StorageNotification(ABC):

    @abstractmethod
    async def add_notification(self, id: int, bucket: str, events: list[str], prefix: str = None, suffix: str = None):
        pass

    @abstractmethod
    async def remove_notification(self, id: int, bucket: str):
        pass
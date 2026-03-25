from abc import ABC, abstractmethod


class Socket(ABC):

    @abstractmethod
    async def send_json(self, user_id: int, message: dict):
        pass

    @abstractmethod
    def get_connections(self) -> dict:
        pass
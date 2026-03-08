from abc import ABC, abstractmethod


class DBTransaction(ABC):

    @abstractmethod
    async def __aenter__(self) -> "DBTransaction":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def get(self, model_class, model_id):
        pass

    @abstractmethod
    def add(self, model):
        pass

    @abstractmethod
    async def refresh(self, model):
        pass

    @abstractmethod
    def delete(self, model):
        pass


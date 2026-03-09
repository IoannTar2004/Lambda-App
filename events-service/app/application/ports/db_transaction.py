from abc import ABC, abstractmethod


class DBTransaction(ABC):

    @abstractmethod
    async def __aenter__(self) -> "DBTransaction":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def get_by_id(self, domain_class, model_id):
        pass

    @abstractmethod
    async def get(self, domain, **kwargs):
        pass

    @abstractmethod
    async def insert(self, domain):
        pass

    @abstractmethod
    async def update(self, domain):
        pass

    @abstractmethod
    async def delete(self, domain):
        pass


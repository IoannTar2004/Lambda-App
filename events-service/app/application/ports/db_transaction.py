from abc import ABC, abstractmethod


class DBTransaction(ABC):

    @abstractmethod
    async def __aenter__(self) -> "DBTransaction":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    async def get(self, domain_class, model_id):
        pass

    @abstractmethod
    async def get_by_filters(self, domain, _selections: list[str] | None = None,
                             _joins: list[str] | None = None, **kwargs):
        pass

    @abstractmethod
    async def get_by_query(self, domain_class, sql: str, **kwargs):
        pass

    @abstractmethod

    @abstractmethod
    async def insert(self, domain):
        pass

    @abstractmethod
    async def update(self, domain):
        pass

    @abstractmethod
    async def delete(self, domain):
        pass

    @abstractmethod
    async def delete_by_filters(self, domain_class, **kwargs):
        pass


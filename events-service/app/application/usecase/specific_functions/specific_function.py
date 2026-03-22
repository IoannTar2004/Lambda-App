from abc import ABC, abstractmethod
from typing import Any

from application.commands.create_function_command import CreateFunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction


class SpecificFunction(ABC):

    @abstractmethod
    async def create(self, function_id: int, data: CreateFunctionCommand, tx: DBTransaction, async_req: AsyncRequest = None):
        pass

    @abstractmethod
    async def delete(self, data: Any, async_req: AsyncRequest = None):
        pass
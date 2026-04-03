from abc import ABC, abstractmethod
from typing import Any

from application.commands.create_function_command import CreateFunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction


class SpecificFunction(ABC):

    @abstractmethod
    async def create(self, user_id, function_id: int, data: dict, tx: DBTransaction, async_req: AsyncRequest = None):
        pass

    @abstractmethod
    async def delete(self, function_id: int, tx: DBTransaction, async_req: AsyncRequest = None):
        pass
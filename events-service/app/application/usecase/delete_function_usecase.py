from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.function_config import FunctionConfig
from domain.models.function_header import FunctionHeader


class DeleteFunctionUsecase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, function_id: int):
        async with self.db_transaction as tx:
            await tx.delete_by_filters(FunctionConfig, function_id=function_id)

            function_header: FunctionHeader = await tx.get(FunctionHeader, function_id)
            await tx.delete(function_header)

            await self.async_req.delete("/api/zip/delete-all-archives", "code-service", {
                "user_id": 300904,
                "function_name": function_header.name
            })
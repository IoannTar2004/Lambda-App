from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.function_config import FunctionConfig
from domain.models.function_header import FunctionHeader


class RollbackFunctionUsecase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, function_id: int):
        async with self.db_transaction as tx:
            function_header: FunctionHeader = await tx.get(FunctionHeader, function_id)
            if not function_header:
                raise HTTPException(status_code=404, detail="Function does not exist")
            if function_header.current_version_number == 1:
                raise HTTPException(status_code=409, detail="Cannot rollback. Version number is 1")

            config = await tx.get_by_filters(FunctionConfig,
                                             function_id=function_id,
                                             version_number=function_header.current_version_number)

            await tx.delete(config[0])
            prev_version_number = function_header.current_version_number
            function_header.current_version_number -= 1
            await tx.update(function_header)

            await self.async_req.delete("/api/zip/delete-version", "code-service", {
                "user_id": function_header.user_id,
                "function_name": function_header.name,
                "version_number": prev_version_number,
            }) # TODO заменить на kafka

from fastapi import HTTPException

from application.commands.update_function_command import UpdateFunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.function_config import FunctionConfig
from domain.models.function_header import FunctionHeader


class UpdateFunctionUseCase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, data: UpdateFunctionCommand):
        async with self.db_transaction as tx:
            function_header: FunctionHeader = await tx.get(FunctionHeader, data.id)
            if not function_header:
                raise HTTPException(status_code=404, detail="Function doesn't exist")

            function_header.current_version_number += 1
            await tx.update(function_header)

            function_config = FunctionConfig(function_id=function_header.id,
                                             version_number=function_header.current_version_number,
                                             handler=data.handler,
                                             memory_size=data.memory_size,
                                             timeout=data.timeout
                                             )
            await tx.insert(function_config)
            await self.async_req.post("/api/zip/zip-project", "code-service", {
                "user_id": 300904,
                "project_name": function_header.project_name,
                "function_name": function_header.name,
                "version_number": function_header.current_version_number
            }) # TODO заменить все на Kafka

            return {
                "function_id": function_header.id
            }
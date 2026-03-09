from application.commands.create_function_command import CreateFunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.function_config import FunctionConfig
from domain.models.function_header import FunctionHeader


class CreateFunctionUseCase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, data: CreateFunctionCommand):
        async with self.db_transaction as tx:
            function_header = FunctionHeader(name=data.function_name,
                                             project_name=data.project_name,
                                             current_version_number=1,
                                             user_id=300904
                                             )
            function_header = await tx.insert(function_header)

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
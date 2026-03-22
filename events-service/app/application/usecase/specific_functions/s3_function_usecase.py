from application.commands.create_function_command import CreateFunctionCommand
from application.commands.create_s3_function_command import CreateS3FunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from application.usecase.specific_functions.specific_function import SpecificFunction
from domain.models.s3_function import S3Function


class S3FunctionUsecase(SpecificFunction):

    async def create(self, function_id: int, data: CreateS3FunctionCommand, tx: DBTransaction, async_req: AsyncRequest = None):
        s3_function = S3Function(id=function_id,
                                 bucket=data.bucket,
                                 events=data.events,
                                 prefix=data.prefix,
                                 suffix=data.suffix)
        await tx.insert(s3_function)
        await async_req.post("/api/events-config/create-s3-event", "code-service", {
            "function_id": function_id,
            "bucket": data.bucket,
            "events": data.events,
            "prefix": data.prefix,
            "suffix": data.suffix
        })

    async def delete(self, data: dict, async_req: AsyncRequest = None):
        await async_req.delete("/api/events-config/delete-s3-event", "code-service", data)
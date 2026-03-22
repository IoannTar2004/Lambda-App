from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from application.usecase.specific_functions.specific_function import SpecificFunction
from domain.models.project import Project
from domain.models.function import Function
from domain.models.s3_function import S3Function


class DeleteFunctionUsecase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction, specific_function: SpecificFunction):
        self.async_req = async_req
        self.db_transaction = db_transaction
        self.specific_function = specific_function

    async def execute(self, function_id: int):
        async with self.db_transaction as tx:
            s3_function = await tx.get(S3Function, function_id)
            await tx.delete_by_filters(Function, id=function_id)
            data = {
                "function_id": function_id,
                "bucket": s3_function.bucket,
            }
            await self.specific_function.delete(data, self.async_req)
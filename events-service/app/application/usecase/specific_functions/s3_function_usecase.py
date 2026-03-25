from application.commands.create_s3_function_command import CreateS3FunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from application.ports.storage_notification import StorageNotification
from application.usecase.specific_functions.specific_function import SpecificFunction
from domain.models.s3_function import S3Function


class S3FunctionUsecase(SpecificFunction):

    def __init__(self, storage_notification: StorageNotification):
        self.storage_notification = storage_notification

    async def create(self, function_id: int, data: CreateS3FunctionCommand, tx: DBTransaction, async_req: AsyncRequest = None):
        s3_function = S3Function(id=function_id,
                                 bucket=data.bucket,
                                 events=data.events,
                                 prefix=data.prefix,
                                 suffix=data.suffix)
        await tx.insert(s3_function)
        id = f"lambda_{function_id}"
        await self.storage_notification.add_notification(id, data.bucket, data.events,
                                                         data.prefix, data.suffix)

    async def delete(self, data: dict, async_req: AsyncRequest = None):
        id = f"lambda_{data['function_id']}"
        await self.storage_notification.remove_notification(id, data['bucket'])
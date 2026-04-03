from application.commands.create_s3_function_command import CreateS3FunctionCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from application.ports.storage_notification import StorageNotification
from application.usecase.specific_functions.specific_function import SpecificFunction
from domain.models.s3_function import S3Function


class S3FunctionUsecase(SpecificFunction):

    def __init__(self, storage_notification: StorageNotification):
        self.storage_notification = storage_notification

    async def create(self, user_id: int, function_id: int, data: dict, tx: DBTransaction, async_req: AsyncRequest = None):
        bucket_name = f"{user_id}-{data['bucket']}"
        s3_function = S3Function(id=function_id,
                                 bucket=bucket_name,
                                 events=data["events"],
                                 prefix=data["prefix"],
                                 suffix=data["suffix"])
        await tx.insert(s3_function)
        id = f"lambda_{function_id}"
        await self.storage_notification.add_notification(id, bucket_name, data["events"],
                                                         data["prefix"], data["suffix"])

    async def delete(self, function_id: int, tx: DBTransaction, async_req: AsyncRequest = None):
        id = f"lambda_{function_id}"
        s3_function: S3Function = await tx.get(S3Function, function_id)
        await self.storage_notification.remove_notification(id, s3_function.bucket)
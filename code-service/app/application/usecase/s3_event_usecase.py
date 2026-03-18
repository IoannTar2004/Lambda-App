from application.ports.storage import StorageNotification
from application.usecase.commands.events.create_s3_event_command import CreateS3EventCommand


class S3EventUsecase:

    def __init__(self, storage_notification: StorageNotification):
        self.storage_notification = storage_notification

    async def create(self, data: CreateS3EventCommand):
        id = f"lambda_{data.function_id}"
        await self.storage_notification.add_notification(id, data.bucket, data.events,
                                                         data.prefix, data.suffix)

    async def delete(self, function_id: int, bucket: str):
        id = f"lambda_{function_id}"
        await self.storage_notification.remove_notification(id, bucket)
from application.ports import storage_notification
from application.ports.storage_notification import StorageNotification
from application.usecase.commands.events.create_s3_event_command import CreateS3EventCommand


class CreateS3EventUsecase:

    def __init__(self, storage_notification: StorageNotification):
        self.storage_notification = storage_notification

    async def execute(self, data: CreateS3EventCommand):
        await self.storage_notification.add_notification(data.function_id, data.bucket, data.events,
                                                         data.prefix, data.suffix)
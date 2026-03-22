from fastapi import HTTPException

from application.ports.storage import Storage
from application.usecase.commands.delete_functions_command import DeleteArchivesCommand
from settings import settings


class DeleteAllArchivesUsecase:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, data: DeleteArchivesCommand):
        _, files = await self.storage.listdir(settings.S3_CODE_ARCHIVES_BUCKET, f"{data.user_id}/"
                                                                                f"{data.function_name}/")
        if not files:
            raise HTTPException(status_code=404, detail="No files found.")

        keys = [{"Key": key["Key"]} for key in files]
        await self.storage.delete_objects(settings.S3_CODE_ARCHIVES_BUCKET, keys)
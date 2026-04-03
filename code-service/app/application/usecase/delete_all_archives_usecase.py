from fastapi import HTTPException

from application.ports.storage import Storage
from application.usecase.commands.delete_functions_command import DeleteArchivesCommand
from settings import settings


class DeleteAllArchivesUsecase:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, user_id: int, project_id: int):
        _, files = await self.storage.listdir(settings.S3_CODE_ARCHIVES_BUCKET, f"{user_id}/{project_id}/")
        if not files:
            return

        print(files)
        files = [f["Key"] for f in files]
        print(files)
        await self.storage.delete(settings.S3_CODE_ARCHIVES_BUCKET, files)
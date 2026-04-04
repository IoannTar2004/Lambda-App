from fastapi import HTTPException

from application.ports.storage import Storage
from application.usecase.commands.delete_functions_command import DeleteArchivesCommand
from settings import settings


class DeleteAllUsecase:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, bucket: str, path: str):
        files = await self.storage.recursive_listdir(bucket, path)
        if not files:
            return

        files = [f["Key"] for f in files]
        await self.storage.delete(bucket, files)
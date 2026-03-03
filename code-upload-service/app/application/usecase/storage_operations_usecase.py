from fastapi import UploadFile

from application.ports.async_storage import AsyncStorage
from s3settings import s3_settings


class UserFilesOperationsUseCase:
    def __init__(self, storage: AsyncStorage):
        self.storage = storage

    async def upload(self, file: UploadFile):
        data = file.file.read()
        await self.storage.upload(s3_settings.s3_user_files_bucket, file.filename, data)

    async def download(self, filename: str):
        file = self.storage.download(s3_settings.s3_user_files_bucket, filename)
        return file
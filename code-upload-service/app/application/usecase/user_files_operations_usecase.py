import os.path
from pathlib import Path

from fastapi import UploadFile

from application.ports.async_storage import AsyncStorage
from application.usecase.dto.listdir_dto import ListdirDto
from settings import settings


class UserFilesOperationsUseCase:
    def __init__(self, storage: AsyncStorage):
        self.storage = storage

    async def upload(self, file: UploadFile):
        data = file.file.read()
        await self.storage.upload(settings.S3_USER_FILES_BUCKET, file.filename, data)

    async def download(self, filename: str):
        file = self.storage.download(settings.S3_USER_FILES_BUCKET, filename)
        return file

    async def listdir(self, path: str):
        directories, files = await self.storage.listdir(settings.S3_USER_FILES_BUCKET, path)
        return ListdirDto(
            directories=[Path(d["Prefix"]).name for d in directories],
            files=[{
                "filename": os.path.basename(file["Key"]),
                "last_modified": file["LastModified"],
                "size": int(file["Size"]),
            } for file in files]
        )
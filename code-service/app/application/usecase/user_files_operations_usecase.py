import os.path
from pathlib import Path

from fastapi import UploadFile, HTTPException

from application.ports.storage import Storage
from application.ports.cache import Cache
from infrastructure.web.dto.user_files.listdir_dto import ListdirDto
from settings import settings


class UserFilesOperationsUseCase:
    def __init__(self, storage: Storage, cache: Cache=None):
        self.storage = storage
        self.cache = cache

    async def upload(self, file: UploadFile, directory: str):
        data = file.file.read()
        await self.storage.upload(settings.S3_USER_FILES_BUCKET, directory + "/" + file.filename, data)
        await self.cache.delete("functions:" + directory + "/" + file.filename)

    async def download(self, filename: str):
        if await self.storage.exists(settings.S3_USER_FILES_BUCKET, filename):
            return self.storage.download(settings.S3_USER_FILES_BUCKET, filename)
        raise HTTPException(status_code=404, detail="File not found")

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

    async def delete(self, path: str):
        await self.storage.delete(settings.S3_USER_FILES_BUCKET, path)
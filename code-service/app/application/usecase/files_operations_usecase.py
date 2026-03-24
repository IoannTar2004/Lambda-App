import os.path
from pathlib import Path

from fastapi import UploadFile, HTTPException

from application.ports.storage import Storage
from application.ports.cache import Cache
from infrastructure.web.dto.user_files.listdir_dto import ListdirDto
from settings import settings


class FilesOperationsUseCase:
    def __init__(self, storage: Storage, cache: Cache=None):
        self.storage = storage
        self.cache = cache

    async def upload(self, bucket: str, file: UploadFile, directory: str):
        data = file.file.read()
        await self.storage.upload(bucket, directory + "/" + file.filename, data)
        await self.cache.delete("functions:" + directory + "/" + file.filename)

    async def download(self, bucket: str, filename: str):
        if await self.storage.exists(settings.S3_USER_FILES_BUCKET, filename):
            return self.storage.download(bucket, filename)
        raise HTTPException(status_code=404, detail="File not found")

    async def listdir(self, bucket: str, path: str):
        directories, files = await self.storage.listdir(bucket, path)
        return ListdirDto(
            directories=[Path(d["Prefix"]).name for d in directories],
            files=[{
                "filename": os.path.basename(file["Key"]),
                "last_modified": file["LastModified"],
                "size": int(file["Size"]),
            } for file in files]
        )

    async def delete(self, bucket: str, path: str):
        await self.storage.delete(bucket, path)
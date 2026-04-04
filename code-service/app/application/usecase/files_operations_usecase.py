import os.path
from pathlib import Path

from fastapi import UploadFile, HTTPException

from application.ports.storage import Storage
from infrastructure.web.dto.user_files.listdir_dto import ListdirDto


class FilesOperationsUseCase:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def upload(self, bucket: str, file: UploadFile, directory: str):
        data = file.file.read()
        directory = directory[:-1] if directory.endswith("/") else directory
        await self.storage.upload(bucket, directory + "/" + file.filename, data)

    async def download(self, bucket: str, path: str):
        if await self.storage.exists(bucket, path):
            return self.storage.download(bucket, path)
        raise HTTPException(status_code=404, detail="File not found")

    async def listdir(self, bucket: str, path: str):
        directories, files = await self.storage.listdir(bucket, path + "/")
        return ListdirDto(
            directories=[Path(d["Prefix"]).name for d in directories],
            files=[{
                "filename": os.path.basename(file["Key"]),
                "last_modified": file["LastModified"],
                "size": int(file["Size"]),
            } for file in files]
        )

    async def listdir_all(self, bucket: str, path: str):
        return await self.storage.recursive_listdir(bucket, path)

    async def delete(self, bucket: str, keys: list[str]):
        for i in range(0, len(keys), 1000):
            chunk = keys[i:i + 1000]
            await self.storage.delete(bucket, chunk)

import io
from typing import BinaryIO

from fastapi import HTTPException
from minio import Minio

from application.ports.storage import Storage
from settings import settings


class MinioService(Storage):

    def __init__(self, url, access_key, secret_key, secure=True) -> None:
        self._client = Minio(url, access_key, secret_key, secure=secure)

    def upload(self, bucket: str | None, path: str, data: bytes) -> None:
        binary = io.BytesIO(data)
        self._client.put_object(bucket, path, binary, len(data))

    def download(self, bucket: str | None, path: str) -> bytes:
        data = self._client.get_object(bucket, path)
        chunk_size = 1024 * 1024
        total_size = 0

        while True:
            chunk = data.read(chunk_size)
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > settings.max_file_size_mb:
                raise HTTPException(status_code=413, detail="File size exceeds the limit!")

            yield chunk

    def remove(self, bucket: str | None, path: str) -> None:
        self._client.remove_object(bucket, path)





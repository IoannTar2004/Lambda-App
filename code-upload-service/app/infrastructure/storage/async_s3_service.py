import io
from typing import Any, AsyncGenerator

import aioboto3
from fastapi import HTTPException

from application.ports.async_storage import AsyncStorage
from s3settings import s3_settings


class AsyncS3Service(AsyncStorage):

    def __init__(self, url, access_key, secret_key) -> None:
        self.url = url
        self.session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    async def upload(self, bucket: str | None, path: str, data: bytes) -> None:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            binary = io.BytesIO(data)
            await s3_client.put_object(Bucket=bucket,
                                       Key=path,
                                       Body=binary)

    async def download(self, bucket: str | None, path: str) -> AsyncGenerator[bytes, Any]:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            response = await s3_client.get_object(Bucket=bucket, Key=path)
            chunk_size = 1024 * 1024
            total_size = 0

            while True:
                chunk = await response["Body"].read(chunk_size)
                if not chunk:
                    break
                total_size += len(chunk)
                if total_size > int(s3_settings.max_file_size_mb) * 1024 * 1024:
                    raise HTTPException(status_code=413, detail="File size exceeds the limit!")

                yield chunk

    async def remove(self, bucket: str | None, path: str) -> None:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            await s3_client.remove_object(bucket_name=bucket,
                                          object_name=path)





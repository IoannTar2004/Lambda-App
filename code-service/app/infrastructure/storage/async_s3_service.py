import io
from typing import Any, AsyncGenerator, cast

import aioboto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from mypy_boto3_s3 import S3Client

from application.ports.storage import Storage
from settings import settings


class S3Service(Storage):

    def __init__(self, url, access_key, secret_key) -> None:
        self.url = url
        self.session: aioboto3.Session = aioboto3.Session(
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
            s3_client = cast(S3Client, s3_client)
            response = await s3_client.get_object(Bucket=bucket, Key=path)
            chunk_size = 1024 * 1024
            total_size = 0

            while True:
                chunk = await response["Body"].read(chunk_size)
                if not chunk:
                    break
                total_size += len(chunk)
                if total_size > int(settings.MAX_FILE_SIZE_MB) * 1024 * 1024:
                    raise HTTPException(status_code=413, detail="File size exceeds the limit!")

                yield chunk

    async def delete(self, bucket: str | None, path: str) -> None:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            await s3_client.delete_object(Bucket=bucket,
                                          Key=path)

    async def delete_objects(self, bucket: str | None, list_object: list[str]) -> None:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            await s3_client.delete_objects(Bucket=bucket, Delete={"Objects": list_object})

    async def exists(self, bucket: str | None, path: str) -> bool:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            try:
                await s3_client.head_object(Bucket=bucket, Key=path)
                return True
            except ClientError:
                return False

    async def listdir(self, bucket: str | None, path: str) -> tuple[list[Any], list[Any]]:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            response = await s3_client.list_objects(Bucket=bucket, Prefix=path, Delimiter="/")
            files = response["Contents"] if "Contents" in response else []
            directories = response["CommonPrefixes"] if "CommonPrefixes" in response else []
            return directories, files

    async def recursive_listdir(self, bucket: str | None, path: str) -> list[Any]:
        async with self.session.client("s3", endpoint_url=self.url) as s3_client:
            res = await s3_client.list_objects(Bucket=bucket, Prefix=path)
            return res["Contents"] if "Contents" in res else []



from typing import cast

from mypy_boto3_s3.client import S3Client

from application.ports.storage_notification import StorageNotification
from infrastructure.storage.async_s3_service import S3Service


class AsyncS3NotificationService(StorageNotification):

    def __init__(self, storage: S3Service):
        self.storage = storage


    async def add_notification(self, id: int, bucket: str, events: list[str], prefix: str = None, suffix: str = None):
        async with self.storage.session.client("s3", endpoint_url=self.storage.url) as s3_client:
            s3_client = cast(S3Client, s3_client)
            configurations: dict = await s3_client.get_bucket_notification_configuration(Bucket=bucket)
            configurations.pop("ResponseMetadata")
            queue_configurations = configurations.get("QueueConfigurations", [])
            queue_configurations.append({
                "Id": f"lambda_{id}",
                "QueueArn": "arn:minio:sqs::1:webhook",
                "Events": events,
                "Filter": {
                    "Key": {
                        "FilterRules": [
                            {"Name": "prefix",
                             "Value": prefix},
                            {"Name": "suffix",
                             "Value": suffix}
                        ]
                    }
                }
            })
            configurations["QueueConfigurations"] = queue_configurations

            await s3_client.put_bucket_notification_configuration(Bucket=bucket,
                                                                  NotificationConfiguration=configurations)

    async def remove_notification(self, id: int, bucket: str):
        async with self.storage.session.client("s3", endpoint_url=self.storage.url) as s3_client:
            s3_client = cast(S3Client, s3_client)
            configurations = await s3_client.get_bucket_notification_configuration(Bucket=bucket)
            configurations["QueueConfigurations"] = [q for q in configurations["QueueConfigurations"] if q["Id"] != id]
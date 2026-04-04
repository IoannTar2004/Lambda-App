import aioboto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from application.ports.storage_notification import StorageNotification


class AsyncS3NotificationService(StorageNotification):

    def __init__(self, url, access_key, secret_key) -> None:
        self.url = url
        self.session: aioboto3.Session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )


    async def add_notification(self, id: str, bucket: str, events: list[str], prefix: str = None, suffix: str = None):
        async with self.session.client("minio", endpoint_url=self.url) as s3_client:
            try:
                configurations: dict = await s3_client.get_bucket_notification_configuration(Bucket=bucket)
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == "NoSuchBucket":
                    raise HTTPException(status_code=404, detail="Bucket not found")
            configurations.pop("ResponseMetadata")
            queue_configurations = configurations.get("QueueConfigurations", [])
            queue_configurations.append({
                "Id": id,
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

    async def remove_notification(self, id: str, bucket: str):
        async with self.session.client("minio", endpoint_url=self.url) as s3_client:
            configurations = await s3_client.get_bucket_notification_configuration(Bucket=bucket)
            configurations.pop("ResponseMetadata")
            if "QueueConfigurations" not in configurations:
                return

            configurations["QueueConfigurations"] = [q for q in configurations["QueueConfigurations"] if q["Id"] != id]
            await s3_client.put_bucket_notification_configuration(Bucket=bucket,
                                                                  NotificationConfiguration=configurations)
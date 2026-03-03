from application.ports.async_storage import AsyncStorage
from s3settings import s3_settings


class SaveCodeUseCase:

    def __init__(self, storage: AsyncStorage) -> None:
        self.storage = storage

    async def save(self, filename: str, code: str) -> None:
        await self.storage.upload(s3_settings.s3_user_files_bucket, "1/my_project/" + filename, code.encode("utf-8"))

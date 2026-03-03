from application.ports.async_storage import AsyncStorage
from settings import settings


class SaveCodeUseCase:

    def __init__(self, storage: AsyncStorage) -> None:
        self.storage = storage

    async def save(self, filename: str, code: str) -> None:
        await self.storage.upload(settings.S3_USER_FILES_BUCKET, "1/my_project/" + filename, code.encode("utf-8"))
        # TODO убрать захардкоженный путь

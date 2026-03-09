from application.ports.storage import Storage
from application.ports.cache import Cache
from settings import settings


class SaveCodeUseCase:

    def __init__(self, storage: Storage, cache: Cache) -> None:
        self.storage = storage
        self.cache = cache

    async def save(self, path: str, code: str) -> None:
        await self.storage.upload(settings.S3_USER_FILES_BUCKET, "300904/" + path, code.encode("utf-8"))
        await self.cache.delete("functions:300904:" + path)
        # TODO убрать захардкоженный путь

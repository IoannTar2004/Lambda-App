from fastapi import UploadFile

from application.ports.storage import Storage
from settings import settings


class UploadCodeUseCase:

    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    async def upload_code(self, file: UploadFile):
        data = await file.read()
        self.storage.upload(settings.s3_user_codes_bucket, "1/" + file.filename, data)
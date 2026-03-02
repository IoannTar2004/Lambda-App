from fastapi import UploadFile

from application.ports.storage import Storage
from settings import settings


class SaveCodeUseCase:

    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def save(self, filename: str, code: str) -> None:
        self.storage.upload(settings.s3_user_codes_bucket, "1/" + filename, code.encode("utf-8"))

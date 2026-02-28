from abc import ABC, abstractmethod
from typing import BinaryIO


class Storage(ABC):

    @abstractmethod
    def upload(self, bucket: str | None, path: str, data: bytes) -> None:
        pass

    @abstractmethod
    def download(self, bucket: str | None, path: str) -> bytes:
        pass

    @abstractmethod
    def remove(self, bucket: str | None, path: str) -> None:
        pass

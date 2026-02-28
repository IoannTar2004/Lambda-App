from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    def upload(self):
        pass

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def delete(self):
        pass

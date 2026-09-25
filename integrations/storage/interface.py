from abc import ABC, abstractmethod
from .models import StorageStatus


class PrivateStorageProvider(ABC):
    @abstractmethod
    def status(self) -> StorageStatus: ...

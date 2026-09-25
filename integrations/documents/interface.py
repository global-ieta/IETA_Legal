from abc import ABC, abstractmethod
from .models import ScanResult


class DocumentSafetyProvider(ABC):
    @abstractmethod
    def scan(self, *, file_name: str, content_type: str, size: int) -> ScanResult: ...

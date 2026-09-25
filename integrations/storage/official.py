from .interface import PrivateStorageProvider
from .models import StorageStatus


class OfficialPrivateStorageProvider(PrivateStorageProvider):
    """Placeholder for an owner-supplied private cloud storage adapter."""
    def __init__(self, backend: str):
        self.backend = backend

    def status(self) -> StorageStatus:
        return StorageStatus(backend=self.backend, private=True, operational=False, production_ready=False)

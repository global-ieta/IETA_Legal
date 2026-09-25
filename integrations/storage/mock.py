from .interface import PrivateStorageProvider
from .models import StorageStatus


class LocalPrivateStorageProvider(PrivateStorageProvider):
    """Development filesystem storage; it has no public URL but is not production storage."""
    def status(self) -> StorageStatus:
        return StorageStatus(backend="local-private-filesystem", private=True, operational=True, production_ready=False)

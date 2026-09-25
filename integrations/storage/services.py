from django.conf import settings
from .interface import PrivateStorageProvider
from .mock import LocalPrivateStorageProvider
from .official import OfficialPrivateStorageProvider


def get_private_storage_provider() -> PrivateStorageProvider:
    if settings.PRIVATE_STORAGE_BACKEND == "local":
        return LocalPrivateStorageProvider()
    return OfficialPrivateStorageProvider(settings.PRIVATE_STORAGE_BACKEND)

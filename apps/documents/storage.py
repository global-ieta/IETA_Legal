from django.conf import settings
from django.core.files.storage import FileSystemStorage

class PrivateDocumentStorage(FileSystemStorage):
    """Development storage with no public URL; replace with private cloud storage later."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", settings.MEDIA_ROOT / "private-documents")
        kwargs.setdefault("base_url", None)
        super().__init__(*args, **kwargs)

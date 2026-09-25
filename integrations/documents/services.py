from django.conf import settings
from .adapter import OfficialDocumentSafetyProvider
from .client import DocumentSafetyClient
from .interface import DocumentSafetyProvider
from .mock import MockDocumentSafetyProvider


def get_document_safety_provider() -> DocumentSafetyProvider:
    if settings.DOCUMENT_SCANNING_API_BASE_URL and settings.DOCUMENT_SCANNING_API_KEY:
        return OfficialDocumentSafetyProvider(DocumentSafetyClient(settings.DOCUMENT_SCANNING_API_BASE_URL, settings.DOCUMENT_SCANNING_API_KEY))
    return MockDocumentSafetyProvider()

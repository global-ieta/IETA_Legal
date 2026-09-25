from .client import DocumentSafetyClient
from .interface import DocumentSafetyProvider


class OfficialDocumentSafetyProvider(DocumentSafetyProvider):
    def __init__(self, client: DocumentSafetyClient):
        self.client = client

    def scan(self, *, file_name: str, content_type: str, size: int):
        return self.client.scan(file_name=file_name, content_type=content_type, size=size)

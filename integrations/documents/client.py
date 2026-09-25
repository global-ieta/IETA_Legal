from .exceptions import DocumentSafetyIntegrationUnavailable
from .models import ScanResult


class DocumentSafetyClient:
    """Placeholder until the owner supplies scanner transport and result fields."""
    def __init__(self, base_url="", api_key=""):
        self.base_url = base_url
        self.api_key = api_key

    def scan(self, *, file_name: str, content_type: str, size: int) -> ScanResult:
        raise DocumentSafetyIntegrationUnavailable("The document safety contract is awaiting owner configuration.")

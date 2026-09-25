from .interface import DocumentSafetyProvider
from .models import ScanResult


class MockDocumentSafetyProvider(DocumentSafetyProvider):
    """Development-only state marker; it does not inspect file content."""
    def scan(self, *, file_name: str, content_type: str, size: int) -> ScanResult:
        return ScanResult(
            status="manual-review-required",
            metadata={"automated_scan": False, "file_name": file_name, "content_type": content_type, "size": size},
        )

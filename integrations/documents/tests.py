from django.test import SimpleTestCase, override_settings

from .adapter import OfficialDocumentSafetyProvider
from .client import DocumentSafetyClient
from .exceptions import DocumentSafetyIntegrationUnavailable
from .services import get_document_safety_provider


class DocumentSafetyIntegrationTests(SimpleTestCase):
    @override_settings(DOCUMENT_SCANNING_API_BASE_URL="", DOCUMENT_SCANNING_API_KEY="")
    def test_development_provider_marks_upload_for_manual_review(self):
        result = get_document_safety_provider().scan(file_name="facts.pdf", content_type="application/pdf", size=10)

        self.assertEqual(result.status, "manual-review-required")
        self.assertFalse(result.metadata["automated_scan"])

    def test_official_placeholder_fails_closed(self):
        provider = OfficialDocumentSafetyProvider(DocumentSafetyClient("https://scanner.example", "test-key"))

        with self.assertRaises(DocumentSafetyIntegrationUnavailable):
            provider.scan(file_name="facts.pdf", content_type="application/pdf", size=10)

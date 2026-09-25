from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from apps.matters.models import Matter
from apps.audit.models import AuditEvent
from .models import PrivateDocument

class PrivateDocumentAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create(username="document_owner")
        self.other = User.objects.create(username="document_other")
        self.matter = Matter.objects.create(owner=self.owner, title="Private matter")
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.owner.pk
        session.save()

    def tearDown(self):
        for document in PrivateDocument.objects.all():
            if document.file:
                document.file.delete(save=False)

    def test_owner_can_upload_and_download_private_document(self):
        upload = SimpleUploadedFile("facts.pdf", b"%PDF-development", content_type="application/pdf")
        response = self.client.post(reverse("documents:upload") + f"?matter_id={self.matter.pk}", {"file": upload})
        self.assertRedirects(response, f"/documents/?matter_id={self.matter.pk}")
        document = PrivateDocument.objects.get(matter=self.matter)
        self.assertEqual(document.status, PrivateDocument.Status.PENDING_REVIEW)
        self.assertTrue(AuditEvent.objects.filter(action="document.uploaded", object_id=str(document.pk)).exists())
        self.assertEqual(self.client.get(reverse("documents:download", args=[document.pk])).status_code, 404)

    def test_unrelated_user_cannot_download_document(self):
        document = PrivateDocument.objects.create(matter=self.matter, uploaded_by=self.owner, original_name="facts.pdf", content_type="application/pdf", size=4, file=SimpleUploadedFile("facts.pdf", b"data", content_type="application/pdf"))
        session = self.client.session
        session["demo_user_id"] = self.other.pk
        session.save()
        self.assertEqual(self.client.get(reverse("documents:download", args=[document.pk])).status_code, 404)

    def test_executable_extension_is_rejected(self):
        upload = SimpleUploadedFile("script.exe", b"MZ", content_type="application/octet-stream")
        response = self.client.post(reverse("documents:upload") + f"?matter_id={self.matter.pk}", {"file": upload})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PrivateDocument.objects.exists())

    @override_settings(DOCUMENT_SCANNING_API_BASE_URL="https://scanner.example", DOCUMENT_SCANNING_API_KEY="test-key")
    def test_configured_scanner_fails_closed_before_storage(self):
        upload = SimpleUploadedFile("facts.pdf", b"%PDF-development", content_type="application/pdf")

        response = self.client.post(reverse("documents:upload") + f"?matter_id={self.matter.pk}", {"file": upload})

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "Document scanning is not configured yet", status_code=503)
        self.assertFalse(PrivateDocument.objects.exists())

    @override_settings(PRIVATE_STORAGE_BACKEND="azure_blob")
    def test_unavailable_private_storage_fails_closed_before_storage(self):
        upload = SimpleUploadedFile("facts.pdf", b"%PDF-development", content_type="application/pdf")

        response = self.client.post(reverse("documents:upload") + f"?matter_id={self.matter.pk}", {"file": upload})

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "Private document storage is not configured yet", status_code=503)
        self.assertFalse(PrivateDocument.objects.exists())

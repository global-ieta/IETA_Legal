from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from apps.documents.models import PrivateDocument
from apps.audit.models import AuditEvent
from apps.matters.models import Matter
from apps.privacy.models import PrivacyRequest

class AdminReviewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create(username="review_owner")
        self.admin = User.objects.create(username="review_admin")
        self.matter = Matter.objects.create(owner=self.owner, title="Review matter")
        self.document = PrivateDocument.objects.create(matter=self.matter, uploaded_by=self.owner, original_name="review.pdf", content_type="application/pdf", size=4, file=SimpleUploadedFile("review.pdf", b"data", content_type="application/pdf"))

    def tearDown(self):
        for document in PrivateDocument.objects.all():
            if document.file:
                document.file.delete(save=False)

    def test_admin_approval_makes_document_available(self):
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()
        response = self.client.post(reverse("admin_portal:review_document", args=[self.document.pk, "approve"]))
        self.assertRedirects(response, reverse("admin_portal:documents"))
        self.document.refresh_from_db()
        self.assertEqual(self.document.status, PrivateDocument.Status.AVAILABLE)

    @override_settings(DOCUMENT_SCANNING_API_BASE_URL="https://scanner.example", DOCUMENT_SCANNING_API_KEY="test-key")
    def test_admin_approval_is_blocked_until_scanner_contract_exists(self):
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()

        response = self.client.post(reverse("admin_portal:review_document", args=[self.document.pk, "approve"]), follow=True)

        self.assertContains(response, "approval is blocked until its contract is reviewed")
        self.document.refresh_from_db()
        self.assertEqual(self.document.status, PrivateDocument.Status.PENDING_REVIEW)

    def test_user_cannot_review_documents(self):
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.owner.pk
        session.save()
        response = self.client.post(reverse("admin_portal:review_document", args=[self.document.pk, "approve"]))
        self.assertRedirects(response, reverse("auth_login"))
        self.document.refresh_from_db()
        self.assertEqual(self.document.status, PrivateDocument.Status.PENDING_REVIEW)

    def test_admin_can_view_non_secret_integration_status(self):
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()

        response = self.client.get(reverse("admin_portal:integration_status"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AURA")
        self.assertContains(response, "Development-Mock")

    def test_user_cannot_view_integration_status(self):
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.owner.pk
        session.save()

        response = self.client.get(reverse("admin_portal:integration_status"))

        self.assertRedirects(response, reverse("auth_login"))

    def test_admin_can_update_privacy_request_status(self):
        privacy_request = PrivacyRequest.objects.create(user=self.owner, request_type=PrivacyRequest.RequestTypes.ACCESS, note="Review my data request.")
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()
        response = self.client.post(reverse("admin_portal:review_privacy_request", args=[privacy_request.pk, "review"]))
        self.assertRedirects(response, reverse("admin_portal:privacy_requests"))
        privacy_request.refresh_from_db()
        self.assertEqual(privacy_request.status, PrivacyRequest.Status.UNDER_REVIEW)

    def test_terminal_privacy_request_cannot_be_changed(self):
        privacy_request = PrivacyRequest.objects.create(user=self.owner, request_type=PrivacyRequest.RequestTypes.ACCESS, status=PrivacyRequest.Status.COMPLETED)
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()

        response = self.client.post(reverse("admin_portal:review_privacy_request", args=[privacy_request.pk, "review"]), follow=True)

        self.assertContains(response, "already in a terminal state")
        privacy_request.refresh_from_db()
        self.assertEqual(privacy_request.status, PrivacyRequest.Status.COMPLETED)

    def test_terminal_privacy_request_is_read_only_in_queue(self):
        privacy_request = PrivacyRequest.objects.create(user=self.owner, request_type=PrivacyRequest.RequestTypes.ACCESS, status=PrivacyRequest.Status.COMPLETED)
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()

        response = self.client.get(reverse("admin_portal:privacy_requests") + "?status=COMPLETED")

        self.assertContains(response, "Closed · no further actions")

    def test_privacy_queue_defaults_to_open_and_supports_status_filter(self):
        completed_user = get_user_model().objects.create(username="completed_privacy_owner")
        PrivacyRequest.objects.create(user=self.owner, request_type=PrivacyRequest.RequestTypes.ACCESS)
        PrivacyRequest.objects.create(user=completed_user, request_type=PrivacyRequest.RequestTypes.DELETION, status=PrivacyRequest.Status.COMPLETED)
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()

        open_response = self.client.get(reverse("admin_portal:privacy_requests"))
        completed_response = self.client.get(reverse("admin_portal:privacy_requests") + "?status=COMPLETED")

        self.assertContains(open_response, "review_owner")
        self.assertNotContains(open_response, "completed_privacy_owner")
        self.assertContains(completed_response, "completed_privacy_owner")

    def test_audit_log_supports_action_filter(self):
        AuditEvent.objects.create(actor=self.admin, action="call.started", object_type="CallSession", object_id="1")
        AuditEvent.objects.create(actor=self.admin, action="call.ended", object_type="CallSession", object_id="1")
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()

        response = self.client.get(reverse("admin_portal:audit_log") + "?action=call.started")

        self.assertEqual([event.action for event in response.context["events"].object_list], ["call.started"])

    def test_audit_log_supports_request_id_filter(self):
        AuditEvent.objects.create(actor=self.admin, action="message.sent", request_id="ticket-42")
        AuditEvent.objects.create(actor=self.admin, action="document.uploaded", request_id="ticket-99")
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = self.admin.pk
        session.save()

        response = self.client.get(reverse("admin_portal:audit_log") + "?request_id=ticket-42")

        self.assertEqual([event.request_id for event in response.context["events"].object_list], ["ticket-42"])

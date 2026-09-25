from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.audit.models import AuditEvent
from .models import Consent, PrivacyRequest

class PrivacyCentreTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="privacy_user")
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.user.pk
        session.save()

    def test_consent_is_versioned_and_updated(self):
        response = self.client.post(reverse("privacy:update_consent"), {"purpose": "aura_intake", "granted": "on"})
        self.assertRedirects(response, reverse("privacy:center"))
        consent = Consent.objects.get(user=self.user, purpose="aura_intake")
        self.assertTrue(consent.granted)
        self.assertEqual(consent.version, "development-1")
        self.assertTrue(AuditEvent.objects.filter(action="privacy.consent.updated").exists())

    def test_privacy_request_is_recorded_without_deleting_data(self):
        response = self.client.post(reverse("privacy:create_request"), {"request_type": "DELETION", "note": "Please review this request."})
        self.assertRedirects(response, reverse("privacy:center"))
        request = PrivacyRequest.objects.get(user=self.user)
        self.assertEqual(request.status, PrivacyRequest.Status.REQUESTED)
        self.assertTrue(AuditEvent.objects.filter(action="privacy.request.created").exists())

    def test_invalid_consent_purpose_does_not_create_record(self):
        self.client.post(reverse("privacy:update_consent"), {"purpose": "unknown", "granted": "on"})
        self.assertFalse(Consent.objects.exists())

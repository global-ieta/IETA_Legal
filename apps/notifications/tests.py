from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from apps.privacy.models import Consent
from apps.audit.models import AuditEvent
from .models import Notification
from .services import get_notification_delivery_policy

class NotificationAccessTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="notification_user")
        self.notification = Notification.objects.create(recipient=self.user, title="Test signal", body="A workflow update.")
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.user.pk
        session.save()

    def test_recipient_can_mark_notification_read(self):
        response = self.client.post(reverse("notifications:mark_read", args=[self.notification.pk]))
        self.assertRedirects(response, reverse("notifications:inbox"))
        self.notification.refresh_from_db()
        self.assertIsNotNone(self.notification.read_at)
        self.assertTrue(AuditEvent.objects.filter(action="notification.read", object_id=str(self.notification.pk)).exists())

    def test_other_user_cannot_mark_notification_read(self):
        other = get_user_model().objects.create(username="other_notification_user")
        session = self.client.session
        session["demo_user_id"] = other.pk
        session.save()
        response = self.client.post(reverse("notifications:mark_read", args=[self.notification.pk]))
        self.assertEqual(response.status_code, 404)

    def test_inbox_explains_in_app_delivery_boundary(self):
        response = self.client.get(reverse("notifications:inbox"))

        self.assertContains(response, "In-app notifications are active.")
        self.assertContains(response, "Email and SMS delivery are not connected.")

    @override_settings(NOTIFICATIONS_API_BASE_URL="https://notify.example", NOTIFICATIONS_API_KEY="test-key")
    def test_external_delivery_requires_provider_and_consent(self):
        policy = get_notification_delivery_policy(self.user.pk)
        self.assertFalse(policy["external_ready"])

    def test_mark_all_read_records_count_without_notification_body(self):
        Notification.objects.create(recipient=self.user, title="Second signal", body="Another workflow update.")

        response = self.client.post(reverse("notifications:mark_all_read"))

        self.assertRedirects(response, reverse("notifications:inbox"))
        event = AuditEvent.objects.get(action="notifications.read_all")
        self.assertEqual(event.metadata["count"], 2)
        self.assertEqual(event.object_id, "")
        Consent.objects.create(user=self.user, purpose="notifications", granted=True, version="development-1")

        policy = get_notification_delivery_policy(self.user.pk)

        self.assertFalse(policy["external_ready"])

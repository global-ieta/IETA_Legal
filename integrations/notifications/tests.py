from django.test import SimpleTestCase, override_settings

from .services import get_notification_delivery_provider


class NotificationDeliveryIntegrationTests(SimpleTestCase):
    @override_settings(NOTIFICATIONS_API_BASE_URL="", NOTIFICATIONS_API_KEY="")
    def test_development_provider_is_in_app_only(self):
        status = get_notification_delivery_provider().status()

        self.assertEqual(status.provider, "in-app-only")
        self.assertTrue(status.in_app_available)
        self.assertFalse(status.external_delivery_available)

    @override_settings(NOTIFICATIONS_API_BASE_URL="https://notify.example", NOTIFICATIONS_API_KEY="test-key")
    def test_official_provider_does_not_claim_external_delivery_before_contract(self):
        status = get_notification_delivery_provider().status()

        self.assertEqual(status.provider, "official-notification-delivery")
        self.assertTrue(status.in_app_available)
        self.assertFalse(status.external_delivery_available)

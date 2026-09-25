from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings
from django.urls import reverse
from apps.consultations.models import Consultation
from apps.messaging.models import Conversation

class CoreTests(TestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_readiness_checks_database_and_cache(self):
        response = self.client.get(reverse("health_ready"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ready")
        self.assertEqual(response.json()["checks"], {"database": "ok", "cache": "ok"})

    def test_request_id_is_returned_and_bounded(self):
        response = self.client.get(reverse("health"), HTTP_X_REQUEST_ID="support-ticket-123")
        self.assertEqual(response.headers["X-Request-ID"], "support-ticket-123")

    def test_integration_report_is_non_networking_and_uses_development_modes(self):
        response = self.client.get(reverse("health_integrations"))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["network_calls"])
        self.assertEqual(response.json()["integrations"]["aura"]["implementation"], "development-mock")
        self.assertEqual(response.json()["integrations"]["global_ieta"]["implementation"], "development-mock")
        self.assertEqual(response.json()["integrations"]["calling"]["implementation"], "development-mock")
        self.assertEqual(response.json()["integrations"]["notification_delivery"]["implementation"], "development-in-app")

    @override_settings(
        AURA_API_BASE_URL="https://aura.example",
        AURA_API_KEY="aura-key",
        GLOBAL_IETA_API_BASE_URL="https://identity.example",
        GLOBAL_IETA_CLIENT_ID="client-id",
        GLOBAL_IETA_CLIENT_SECRET="client-secret",
        CALLING_API_BASE_URL="https://calling.example",
        CALLING_API_KEY="calling-key",
        NOTIFICATIONS_API_BASE_URL="https://notify.example",
        NOTIFICATIONS_API_KEY="notify-key",
    )
    def test_integration_report_marks_complete_configuration_as_contract_pending(self):
        response = self.client.get(reverse("health_integrations"))
        integrations = response.json()["integrations"]

        self.assertEqual(integrations["aura"]["configuration"], "complete")
        self.assertEqual(integrations["aura"]["implementation"], "contract-pending")
        self.assertEqual(integrations["global_ieta"]["implementation"], "contract-pending")
        self.assertEqual(integrations["calling"]["implementation"], "contract-pending")
        self.assertEqual(integrations["notification_delivery"]["implementation"], "contract-pending")

    @override_settings(AURA_ENABLED=False)
    def test_disabled_aura_is_reported_without_being_treated_as_missing(self):
        response = self.client.get(reverse("health_integrations"))
        aura = response.json()["integrations"]["aura"]

        self.assertFalse(aura["enabled"])
        self.assertEqual(aura["configuration"], "disabled")

    @override_settings(DEMO_MODE=True)
    def test_demo_workspace_command_is_idempotent(self):
        call_command("seed_demo_workspace")
        call_command("seed_demo_workspace")
        self.assertEqual(Consultation.objects.count(), 1)
        self.assertEqual(Conversation.objects.count(), 1)

    @override_settings(DEMO_MODE=False)
    def test_demo_workspace_command_is_disabled_in_production_mode(self):
        with self.assertRaises(CommandError):
            call_command("seed_demo_workspace")

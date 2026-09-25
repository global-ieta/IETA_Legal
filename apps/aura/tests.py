from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from integrations.aura.mock import MockAuraProvider
from integrations.aura.prompts import SAFETY_SYSTEM_PROMPT
from integrations.aura.client import AuraClient
from integrations.aura.exceptions import AuraIntegrationUnavailable
from integrations.aura.models import AuraRequest
from integrations.aura.validators import validate_provider_response
from .services import get_aura_provider
from apps.audit.models import AuditEvent
from .models import AuraConversation, AuraMessage

class AuraSafetyTests(TestCase):
    def test_provider_response_validation_rejects_empty_or_oversized_output(self):
        with self.assertRaises(ValueError):
            validate_provider_response(" ")
        with self.assertRaises(ValueError):
            validate_provider_response("x" * 10001)

    def test_mock_stays_factual(self):
        response = MockAuraProvider().intake_conversation("I was contacted on Monday")
        self.assertIn("date", response.lower())
        self.assertNotIn("you should file", response.lower())

    def test_server_prompt_sets_non_advisory_boundary(self):
        self.assertIn("do not provide legal advice", SAFETY_SYSTEM_PROMPT.lower())
        self.assertIn("do not recommend", SAFETY_SYSTEM_PROMPT.lower())

    @override_settings(RATE_LIMITS={"aura": 1}, RATE_LIMIT_WINDOW_SECONDS=60)
    def test_aura_is_rate_limited_and_audited(self):
        cache.clear()
        user = get_user_model().objects.create(username="aura_rate_user")
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = user.pk
        session.save()
        first = self.client.post(reverse("aura:message"), {"message": "First factual message"})
        second = self.client.post(reverse("aura:message"), {"message": "Second factual message"})
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 429)
        self.assertEqual(second.headers["X-RateLimit-Limit"], "1")
        self.assertEqual(second.headers["X-RateLimit-Remaining"], "0")
        self.assertEqual(second.headers["Retry-After"], "60")
        self.assertEqual(AuditEvent.objects.filter(action="aura.message").count(), 1)
        self.assertEqual(AuditEvent.objects.filter(action="aura.rate_limited").count(), 1)

    def test_official_client_does_not_invent_api_contract(self):
        with self.assertRaises(AuraIntegrationUnavailable):
            AuraClient("https://owner.example", "secret", "model").execute(AuraRequest(operation="intake_conversation"))

    @override_settings(AI_PROVIDER="other")
    def test_alternate_ai_provider_is_rejected(self):
        with self.assertRaises(ImproperlyConfigured):
            get_aura_provider()

    @override_settings(AURA_API_BASE_URL="https://owner.example", AURA_API_KEY="owner-key")
    def test_unavailable_official_aura_fails_gracefully(self):
        user = get_user_model().objects.create(username="aura_unavailable_user")
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = user.pk
        session.save()
        response = self.client.post(reverse("aura:message"), {"message": "A factual message"})
        self.assertEqual(response.status_code, 503)
        self.assertTrue(AuditEvent.objects.filter(action="aura.unavailable").exists())

    def test_factual_conversation_persists_across_workspace_requests(self):
        user = get_user_model().objects.create(username="aura_persistent_user")
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = user.pk
        session.save()
        response = self.client.post(reverse("aura:message"), {"message": "The incident happened in a shared development dataset."})
        self.assertEqual(response.status_code, 200)
        conversation = AuraConversation.objects.get(user=user)
        self.assertEqual(AuraMessage.objects.filter(conversation=conversation).count(), 2)
        workspace = self.client.get(reverse("aura:workspace"))
        self.assertContains(workspace, "shared development dataset")

    def test_user_cannot_write_to_another_aura_conversation(self):
        owner = get_user_model().objects.create(username="aura_owner")
        other = get_user_model().objects.create(username="aura_other")
        conversation = AuraConversation.objects.create(user=owner)
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = other.pk
        session.save()
        response = self.client.post(reverse("aura:message"), {"conversation_id": conversation.pk, "message": "Should not be accepted"})
        self.assertEqual(response.status_code, 404)

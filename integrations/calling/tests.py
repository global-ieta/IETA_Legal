from django.test import SimpleTestCase, override_settings

from .adapter import OfficialSignalingProvider
from .client import SignalingClient
from .exceptions import CallingIntegrationUnavailable
from .services import get_signaling_provider


class CallingIntegrationTests(SimpleTestCase):
    @override_settings(CALLING_API_BASE_URL="", CALLING_API_KEY="")
    def test_missing_configuration_uses_non_media_mock(self):
        provider = get_signaling_provider()
        session = provider.create_session(call_id="42", mode="audio")

        self.assertEqual(session.status, "simulated")
        self.assertFalse(session.metadata["media_transmitted"])
        self.assertEqual(session.metadata["call_id"], "42")

    @override_settings(CALLING_API_BASE_URL="https://calling.example", CALLING_API_KEY="test-key")
    def test_complete_configuration_selects_official_boundary(self):
        self.assertIsInstance(get_signaling_provider(), OfficialSignalingProvider)

    def test_placeholder_official_client_fails_closed(self):
        with self.assertRaises(CallingIntegrationUnavailable):
            OfficialSignalingProvider(SignalingClient("https://calling.example", "test-key")).create_session(call_id="42", mode="video")

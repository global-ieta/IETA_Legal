from django.test import SimpleTestCase, override_settings
from .client import GlobalIetaClient
from .exceptions import IdentityIntegrationUnavailable
from .models import ExternalIdentity
from .services import get_identity_provider

class GlobalIetaBoundaryTests(SimpleTestCase):
    def test_client_does_not_invent_identity_contract(self):
        with self.assertRaises(IdentityIntegrationUnavailable):
            GlobalIetaClient("https://owner.example", "client", "secret").resolve_identity(ExternalIdentity("subject"))

    @override_settings(GLOBAL_IETA_API_BASE_URL="", GLOBAL_IETA_CLIENT_ID="", GLOBAL_IETA_CLIENT_SECRET="")
    def test_missing_contract_uses_development_mock(self):
        result = get_identity_provider().resolve_identity("development-subject")
        self.assertEqual(result["status"], "development-only")

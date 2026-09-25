from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from integrations.aura.adapter import OfficialAuraProvider
from integrations.aura.client import AuraClient
from integrations.aura.interface import AIProvider
from integrations.aura.mock import MockAuraProvider

def get_aura_provider() -> AIProvider:
    """Select mock or official AURA only; no alternate AI providers are supported."""
    if settings.AI_PROVIDER.lower() != "aura":
        raise ImproperlyConfigured("IETA Legal supports only the AURA provider.")
    if settings.AURA_API_BASE_URL and settings.AURA_API_KEY:
        return OfficialAuraProvider(AuraClient(settings.AURA_API_BASE_URL, settings.AURA_API_KEY, settings.AURA_MODEL))
    return MockAuraProvider()

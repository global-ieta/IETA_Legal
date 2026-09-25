from django.conf import settings
from .adapter import OfficialIdentityProvider
from .client import GlobalIetaClient
from .interface import IdentityProvider
from .mock import MockIdentityProvider

def get_identity_provider() -> IdentityProvider:
    if settings.GLOBAL_IETA_API_BASE_URL and settings.GLOBAL_IETA_CLIENT_ID and settings.GLOBAL_IETA_CLIENT_SECRET:
        return OfficialIdentityProvider(GlobalIetaClient(settings.GLOBAL_IETA_API_BASE_URL, settings.GLOBAL_IETA_CLIENT_ID, settings.GLOBAL_IETA_CLIENT_SECRET))
    return MockIdentityProvider()

from django.conf import settings
from .adapter import OfficialSignalingProvider
from .client import SignalingClient
from .interface import SignalingProvider
from .mock import MockSignalingProvider

def get_signaling_provider() -> SignalingProvider:
    if settings.CALLING_API_BASE_URL and settings.CALLING_API_KEY:
        return OfficialSignalingProvider(SignalingClient(settings.CALLING_API_BASE_URL, settings.CALLING_API_KEY))
    return MockSignalingProvider()

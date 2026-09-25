from django.conf import settings


def _contract(configured, *, enabled=True):
    if not enabled:
        return {
            "enabled": False,
            "configuration": "disabled",
            "implementation": "disabled",
        }
    return {
        "enabled": True,
        "configuration": "complete" if configured else "missing",
        "implementation": "contract-pending" if configured else "development-mock",
    }


def get_integration_readiness():
    """Return a non-secret, local configuration report without network calls."""
    storage_configured = settings.PRIVATE_STORAGE_BACKEND != "local"
    return {
        "aura": _contract(
            bool(settings.AURA_API_BASE_URL and settings.AURA_API_KEY),
            enabled=settings.AURA_ENABLED,
        ),
        "global_ieta": _contract(
            bool(
                settings.GLOBAL_IETA_API_BASE_URL
                and settings.GLOBAL_IETA_CLIENT_ID
                and settings.GLOBAL_IETA_CLIENT_SECRET
            ),
        ),
        "calling": _contract(
            bool(settings.CALLING_API_BASE_URL and settings.CALLING_API_KEY),
        ),
        "document_scanning": _contract(
            bool(settings.DOCUMENT_SCANNING_API_BASE_URL and settings.DOCUMENT_SCANNING_API_KEY),
        ),
        "private_storage": {
            "enabled": True,
            "configuration": "selected" if storage_configured else "local-development",
            "implementation": "contract-pending" if storage_configured else "development-filesystem",
        },
        "notification_delivery": {
            "enabled": True,
            "configuration": "complete" if settings.NOTIFICATIONS_API_BASE_URL and settings.NOTIFICATIONS_API_KEY else "missing",
            "implementation": "contract-pending" if settings.NOTIFICATIONS_API_BASE_URL and settings.NOTIFICATIONS_API_KEY else "development-in-app",
        },
    }

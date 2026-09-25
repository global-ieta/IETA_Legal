from .models import Notification
from apps.privacy.models import Consent
from integrations.notifications.services import get_notification_delivery_provider


def create_in_app_notification(*, recipient_id, kind, title, body):
    """Create a recipient-scoped in-app notification without implying external delivery."""
    return Notification.objects.create(recipient_id=recipient_id, kind=kind, title=title, body=body)


def get_notification_delivery_policy(recipient_id):
    provider_status = get_notification_delivery_provider().status()
    consent_granted = Consent.objects.filter(
        user_id=recipient_id,
        purpose="notifications",
        granted=True,
    ).exists()
    return {
        "provider": provider_status.provider,
        "in_app_available": provider_status.in_app_available,
        "consent_granted": consent_granted,
        "external_ready": provider_status.external_delivery_available and consent_granted,
    }

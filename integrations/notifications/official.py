from .interface import NotificationDeliveryProvider
from .models import DeliveryStatus


class OfficialNotificationProvider(NotificationDeliveryProvider):
    """Placeholder for owner-supplied email/SMS delivery infrastructure."""
    def __init__(self, base_url: str):
        self.base_url = base_url

    def status(self) -> DeliveryStatus:
        return DeliveryStatus(provider="official-notification-delivery", in_app_available=True, external_delivery_available=False)

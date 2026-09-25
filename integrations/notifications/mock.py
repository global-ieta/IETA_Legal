from .interface import NotificationDeliveryProvider
from .models import DeliveryStatus


class InAppOnlyNotificationProvider(NotificationDeliveryProvider):
    """Development policy: persist notifications in-app, with no external delivery."""
    def status(self) -> DeliveryStatus:
        return DeliveryStatus(provider="in-app-only", in_app_available=True, external_delivery_available=False)

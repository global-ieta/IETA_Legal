from django.conf import settings
from .interface import NotificationDeliveryProvider
from .mock import InAppOnlyNotificationProvider
from .official import OfficialNotificationProvider


def get_notification_delivery_provider() -> NotificationDeliveryProvider:
    if settings.NOTIFICATIONS_API_BASE_URL and settings.NOTIFICATIONS_API_KEY:
        return OfficialNotificationProvider(settings.NOTIFICATIONS_API_BASE_URL)
    return InAppOnlyNotificationProvider()

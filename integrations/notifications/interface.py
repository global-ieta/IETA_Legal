from abc import ABC, abstractmethod
from .models import DeliveryStatus


class NotificationDeliveryProvider(ABC):
    @abstractmethod
    def status(self) -> DeliveryStatus: ...

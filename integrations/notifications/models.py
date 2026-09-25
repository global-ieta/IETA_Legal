from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryStatus:
    provider: str
    in_app_available: bool
    external_delivery_available: bool

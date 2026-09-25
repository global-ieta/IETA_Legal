from .exceptions import CallingIntegrationUnavailable
from .models import SignalingSession

class SignalingClient:
    """Placeholder for the official signaling/TURN contract."""
    def __init__(self, base_url="", api_key=""):
        self.base_url = base_url
        self.api_key = api_key

    def create_session(self, *, call_id: str, mode: str) -> SignalingSession:
        raise CallingIntegrationUnavailable("The official calling/signaling contract is awaiting owner configuration.")

    def close_session(self, *, session_id: str) -> None:
        raise CallingIntegrationUnavailable("The official calling/signaling contract is awaiting owner configuration.")

import uuid
from .interface import SignalingProvider
from .models import SignalingSession

class MockSignalingProvider(SignalingProvider):
    """Development-only state simulation; it never transmits media."""
    def create_session(self, *, call_id: str, mode: str) -> SignalingSession:
        return SignalingSession(session_id=f"dev-{uuid.uuid4().hex}", mode=mode, status="simulated", metadata={"call_id": call_id, "media_transmitted": False})

    def close_session(self, *, session_id: str) -> None:
        return None

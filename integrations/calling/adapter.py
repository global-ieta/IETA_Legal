from .client import SignalingClient
from .interface import SignalingProvider

class OfficialSignalingProvider(SignalingProvider):
    def __init__(self, client: SignalingClient):
        self.client = client

    def create_session(self, *, call_id: str, mode: str):
        return self.client.create_session(call_id=call_id, mode=mode)

    def close_session(self, *, session_id: str):
        return self.client.close_session(session_id=session_id)

from abc import ABC, abstractmethod
from .models import SignalingSession

class SignalingProvider(ABC):
    @abstractmethod
    def create_session(self, *, call_id: str, mode: str) -> SignalingSession: ...

    @abstractmethod
    def close_session(self, *, session_id: str) -> None: ...

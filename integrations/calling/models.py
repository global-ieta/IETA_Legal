from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class SignalingSession:
    session_id: str
    mode: str
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)

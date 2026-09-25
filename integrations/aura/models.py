from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class AuraRequest:
    operation: str
    message: str = ""
    context: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class AuraResponse:
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)

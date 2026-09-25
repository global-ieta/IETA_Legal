from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ScanResult:
    status: str
    metadata: dict[str, Any] = field(default_factory=dict)

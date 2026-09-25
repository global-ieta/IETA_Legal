from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class ExternalIdentity:
    subject: str
    claims: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class IdentitySession:
    subject: str
    status: str
    claims: dict[str, Any] = field(default_factory=dict)

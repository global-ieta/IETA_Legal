from dataclasses import dataclass


@dataclass(frozen=True)
class StorageStatus:
    backend: str
    private: bool
    operational: bool
    production_ready: bool

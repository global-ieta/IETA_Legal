from abc import ABC, abstractmethod
class IdentityProvider(ABC):
    @abstractmethod
    def resolve_identity(self, external_subject): ...

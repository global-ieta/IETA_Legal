from abc import ABC, abstractmethod


class AuthenticationProvider(ABC):
    @abstractmethod
    def authenticate(self, identifier: str, password: str): ...

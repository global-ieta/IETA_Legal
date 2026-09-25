from integrations.global_ieta.exceptions import IdentityIntegrationUnavailable
from ..interfaces import AuthenticationProvider


class GlobalIetaAuthenticationProvider(AuthenticationProvider):
    """Fail-closed authentication boundary until the official identity contract exists."""

    def authenticate(self, identifier: str, password: str):
        raise IdentityIntegrationUnavailable("The official Global IETA identity contract is awaiting owner configuration.")

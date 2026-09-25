from .exceptions import IdentityIntegrationUnavailable
from .models import ExternalIdentity, IdentitySession

class GlobalIetaClient:
    """Placeholder client; no Global IETA endpoint or token contract is assumed."""
    def __init__(self, base_url="", client_id="", client_secret=""):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

    def resolve_identity(self, identity: ExternalIdentity) -> IdentitySession:
        raise IdentityIntegrationUnavailable("The official Global IETA identity contract is awaiting owner configuration.")

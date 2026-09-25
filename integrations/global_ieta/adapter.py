from .client import GlobalIetaClient
from .interface import IdentityProvider
from .models import ExternalIdentity

class OfficialIdentityProvider(IdentityProvider):
    def __init__(self, client: GlobalIetaClient):
        self.client = client

    def resolve_identity(self, external_subject):
        return self.client.resolve_identity(ExternalIdentity(subject=external_subject))

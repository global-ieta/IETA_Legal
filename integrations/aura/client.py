from .exceptions import AuraIntegrationUnavailable
from .models import AuraRequest, AuraResponse

class AuraClient:
    """Placeholder client for the official AURA contract; it makes no invented HTTP request."""
    def __init__(self, base_url="", api_key="", model=""):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

    def execute(self, request: AuraRequest) -> AuraResponse:
        raise AuraIntegrationUnavailable("The official AURA API contract is awaiting owner configuration.")

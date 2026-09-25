from .client import AuraClient
from .interface import AIProvider
from .models import AuraRequest

class OfficialAuraProvider(AIProvider):
    """Application adapter reserved for the owner-supplied AURA API."""
    def __init__(self, client: AuraClient):
        self.client = client

    def intake_conversation(self, message: str) -> str:
        return self.client.execute(AuraRequest(operation="intake_conversation", message=message)).text

    def summarize_facts(self, facts: str) -> str:
        return self.client.execute(AuraRequest(operation="summarize_facts", message=facts)).text

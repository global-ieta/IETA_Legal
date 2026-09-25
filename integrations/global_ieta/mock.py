from .interface import IdentityProvider
class MockIdentityProvider(IdentityProvider):
    def resolve_identity(self, external_subject):
        return {"external_subject": external_subject, "status": "development-only"}

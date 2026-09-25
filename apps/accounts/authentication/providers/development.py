from django.contrib.auth import get_user_model
from django.db.models import Q

from ..interfaces import AuthenticationProvider


class LocalAuthenticationProvider(AuthenticationProvider):
    """Local account provider with Django's password hashing and session model."""
    def authenticate(self, identifier: str, password: str):
        User = get_user_model()
        user = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).first()
        if user and user.is_active and user.check_password(password):
            return user
        return None

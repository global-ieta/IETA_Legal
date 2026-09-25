from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import login, logout

from apps.accounts.models import UserProfile
from .interfaces import AuthenticationProvider
from .providers.development import LocalAuthenticationProvider
from .providers.global_ieta import GlobalIetaAuthenticationProvider


def get_authentication_provider() -> AuthenticationProvider:
    provider_name = getattr(settings, "AUTH_PROVIDER", "development")
    if provider_name == "development":
        return LocalAuthenticationProvider()
    if provider_name == "global_ieta":
        return GlobalIetaAuthenticationProvider()
    raise ImproperlyConfigured("The configured authentication provider is not available.")


def account_role(user):
    profile = UserProfile.objects.filter(user=user).first()
    if profile:
        return profile.role
    return UserProfile.Roles.ADMIN if user.is_staff else UserProfile.Roles.USER


def establish_session(request, user):
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    role = account_role(user)
    request.session["demo_role"] = role
    request.session["demo_user_id"] = user.pk
    request.session["demo_display_name"] = user.get_full_name() or user.username
    return role


def end_session(request):
    logout(request)

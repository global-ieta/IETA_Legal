import re
import uuid

from django.conf import settings

from apps.accounts.models import UserProfile


class DemoRoleMiddleware:
    """Expose role context for authenticated users and local-only compatibility sessions."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(request, "user", None) is not None and request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user).first()
            request.demo_role = profile.role if profile else (UserProfile.Roles.ADMIN if request.user.is_staff else UserProfile.Roles.USER)
            request.demo_user_id = request.user.pk
        elif settings.DEMO_MODE:
            request.demo_role = request.session.get("demo_role")
            request.demo_user_id = request.session.get("demo_user_id")
        return self.get_response(request)


class RequestIDMiddleware:
    """Attach a bounded request identifier for support and log correlation."""

    pattern = re.compile(r"^[A-Za-z0-9._-]{1,64}$")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        incoming = request.headers.get("X-Request-ID", "")
        request.request_id = incoming if self.pattern.match(incoming) else uuid.uuid4().hex
        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id
        return response

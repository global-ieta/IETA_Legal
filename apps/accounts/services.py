from django.conf import settings
from django.contrib.auth import get_user_model
from .models import UserProfile
from apps.advocates.models import AdvocateProfile

DEMO_IDENTITIES = {
    "USER": ("demo_user", "IETA Member"),
    "ADVOCATE": ("demo_advocate", "Independent Advocate"),
    "ADMIN": ("demo_admin", "Operations Admin"),
}

def enter_demo_role(request, role):
    if role not in DEMO_IDENTITIES:
        raise ValueError("Unsupported development role")
    username, display_name = DEMO_IDENTITIES[role]
    user, _ = get_user_model().objects.get_or_create(username=username, defaults={"first_name": display_name})
    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={"role": role, "display_name": display_name})
    if profile.role != role:
        profile.role = role
        profile.save(update_fields=["role"])
    if role == "ADVOCATE":
        AdvocateProfile.objects.get_or_create(
            user=user,
            defaults={
                "display_name": "Independent Advocate",
                "practice_areas": ["Civil information intake", "Consultation preparation"],
                "jurisdictions": ["Jurisdiction to be confirmed"],
                "languages": ["English"],
                "consultation_modes": ["Video", "Audio"],
                "bio": "Professional profile information supplied for advocate discovery.",
                "verified": True,
                "available": True,
            },
        )
    request.session["demo_role"] = role
    request.session["demo_user_id"] = user.pk
    request.session["demo_display_name"] = display_name
    request.session.modified = True
    return profile

def leave_demo_role(request):
    request.session.pop("demo_role", None)
    request.session.pop("demo_user_id", None)
    request.session.pop("demo_display_name", None)

def require_demo_role(request, allowed_roles):
    if not getattr(request.user, "is_authenticated", False) and not settings.DEMO_MODE:
        return False
    role = getattr(request, "demo_role", None)
    return role in allowed_roles

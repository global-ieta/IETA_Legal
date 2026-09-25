from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from apps.core.rate_limit import apply_rate_limit_headers, check_request
from .authentication.services import account_role, end_session, establish_session, get_authentication_provider
from .forms import AccountRegistrationForm, AdvocateProfileSettingsForm, AdvocateRegistrationForm, LoginForm, UserProfileForm
from .models import UserProfile
from apps.advocates.models import AdvocateProfile
from integrations.global_ieta.exceptions import IdentityIntegrationUnavailable
from .services import enter_demo_role


def _safe_next_url(request):
    candidate = request.POST.get("next") or request.GET.get("next")
    if candidate and url_has_allowed_host_and_scheme(candidate, {request.get_host()}, require_https=request.is_secure()):
        return candidate
    return reverse("portal:home")

def entry(request):
    if not settings.DEMO_MODE:
        return render(request, "errors/disabled.html", status=404)
    # Kept as a compatibility endpoint for existing bookmarks; the customer UI uses /login/.
    if request.method == "POST":
        role = request.POST.get("role", "")
        try:
            enter_demo_role(request, role)
        except ValueError:
            messages.error(request, "That sign-in request could not be completed.")
        else:
            return redirect("portal:home")
    return login_view(request)

def exit_demo(request):
    end_session(request)
    return redirect("public:home")


def logout_view(request):
    end_session(request)
    return redirect("public:home")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("portal:home")
    selected_role = request.POST.get("login_role", "") if request.method == "POST" else ""
    selected_role = selected_role if selected_role in {UserProfile.Roles.USER, UserProfile.Roles.ADVOCATE} else ""
    form_prefix = selected_role.lower() if selected_role else ""
    form = LoginForm(request.POST or None, prefix=form_prefix or None)
    user_form = form if selected_role == UserProfile.Roles.USER or not selected_role else LoginForm(prefix="user")
    advocate_form = form if selected_role == UserProfile.Roles.ADVOCATE else LoginForm(prefix="advocate")
    context = {"form": form, "user_form": user_form, "advocate_form": advocate_form, "selected_role": selected_role, "next": request.GET.get("next", "")}
    if request.method == "POST":
        rate_limit = check_request(request, "login")
        if not rate_limit.allowed:
            form.add_error(None, "Too many sign-in attempts. Please wait and try again.")
            context["user_form"] = form if selected_role == UserProfile.Roles.USER or not selected_role else user_form
            context["advocate_form"] = form if selected_role == UserProfile.Roles.ADVOCATE else advocate_form
            response = render(request, "accounts/login.html", context, status=429)
            return apply_rate_limit_headers(response, rate_limit)
    if request.method == "POST" and form.is_valid():
        try:
            user = get_authentication_provider().authenticate(form.cleaned_data["identifier"], form.cleaned_data["password"])
        except IdentityIntegrationUnavailable:
            form.add_error(None, "Sign-in is temporarily unavailable. Please try again later.")
            return render(request, "accounts/login.html", context, status=503)
        if user:
            if selected_role and account_role(user) != selected_role:
                form.add_error(None, "These credentials belong to a different workspace. Select the matching sign-in.")
                return render(request, "accounts/login.html", context)
            establish_session(request, user)
            return redirect(_safe_next_url(request))
        form.add_error(None, "Your login details could not be verified. Please check your credentials and try again.")
    return render(request, "accounts/login.html", context)


def _split_values(value):
    return [item.strip() for item in value.split(",") if item.strip()]


@transaction.atomic
def _create_account(form, role):
    User = get_user_model()
    user = User.objects.create_user(
        username=form.cleaned_data["login_id"],
        email=form.cleaned_data["email"],
        password=form.cleaned_data["password"],
        first_name=form.cleaned_data["display_name"],
    )
    UserProfile.objects.create(user=user, role=role, display_name=form.cleaned_data["display_name"])
    if role == UserProfile.Roles.ADVOCATE:
        AdvocateProfile.objects.create(
            user=user,
            display_name=form.cleaned_data["display_name"],
            practice_areas=_split_values(form.cleaned_data["practice_areas"]),
            jurisdictions=_split_values(form.cleaned_data["jurisdictions"]),
            languages=_split_values(form.cleaned_data["languages"]),
            consultation_modes=_split_values(form.cleaned_data["consultation_modes"]),
        )
    return user


def register(request):
    if request.user.is_authenticated:
        return redirect("portal:home")
    form = AccountRegistrationForm(request.POST or None)
    if settings.AUTH_PROVIDER != "development":
        messages.error(request, "Account registration is temporarily unavailable while official identity access is being connected.")
        return render(request, "accounts/register.html", {"form": form, "account_type": "User account"}, status=503)
    if request.method == "POST" and form.is_valid():
        establish_session(request, _create_account(form, UserProfile.Roles.USER))
        return redirect("portal:home")
    return render(request, "accounts/register.html", {"form": form, "account_type": "User account"})


def register_advocate(request):
    if request.user.is_authenticated:
        return redirect("portal:home")
    form = AdvocateRegistrationForm(request.POST or None)
    if settings.AUTH_PROVIDER != "development":
        messages.error(request, "Advocate registration is temporarily unavailable while official identity access is being connected.")
        return render(request, "accounts/register_advocate.html", {"form": form, "account_type": "Advocate account"}, status=503)
    if request.method == "POST" and form.is_valid():
        establish_session(request, _create_account(form, UserProfile.Roles.ADVOCATE))
        return redirect("portal:home")
    return render(request, "accounts/register_advocate.html", {"form": form, "account_type": "Advocate account"})

def profile(request):
    if not getattr(request, "demo_role", None) or not request.demo_user_id:
        return redirect("auth_login")
    identity = UserProfile.objects.get(user_id=request.demo_user_id)
    advocate = AdvocateProfile.objects.filter(user_id=request.demo_user_id).first()
    identity_form = UserProfileForm(request.POST or None, instance=identity)
    advocate_form = AdvocateProfileSettingsForm(request.POST or None, initial={"display_name": advocate.display_name, "bio": advocate.bio, "available": advocate.available}) if advocate else None
    if request.method == "POST" and identity_form.is_valid() and (not advocate_form or advocate_form.is_valid()):
        identity_form.save()
        if advocate and advocate_form:
            advocate.display_name = advocate_form.cleaned_data["display_name"]
            advocate.bio = advocate_form.cleaned_data["bio"]
            advocate.available = advocate_form.cleaned_data["available"]
            advocate.save(update_fields=["display_name", "bio", "available", "updated_at"])
        request.session["demo_display_name"] = identity.display_name
        messages.success(request, "Your profile was updated.")
        return redirect("accounts_profile:profile")
    return render(request, "portal/profile.html", {"identity_form": identity_form, "advocate_form": advocate_form, "profile": identity, "advocate": advocate})

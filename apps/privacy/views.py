from django.contrib import messages
from django.shortcuts import redirect, render
from apps.accounts.services import require_demo_role
from apps.audit.services import record_event
from .forms import PrivacyRequestForm
from .models import Consent, PrivacyRequest

CONSENT_PURPOSES = {
    "aura_intake": "Use AURA to organise factual intake information",
    "advocate_contact": "Share selected matter information with an authorised advocate",
    "notifications": "Receive workflow notifications inside IETA Legal",
}

def center(request):
    if not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}): return redirect("auth_login")
    return render(request, "portal/privacy_center.html", {"consents": Consent.objects.filter(user_id=request.demo_user_id), "purposes": CONSENT_PURPOSES, "privacy_requests": PrivacyRequest.objects.filter(user_id=request.demo_user_id), "request_form": PrivacyRequestForm()})

def update_consent(request):
    if request.method != "POST" or not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}): return redirect("auth_login")
    purpose = request.POST.get("purpose", "")
    if purpose not in CONSENT_PURPOSES:
        messages.error(request, "That consent purpose is not available.")
        return redirect("privacy:center")
    granted = request.POST.get("granted") == "on"
    consent, _ = Consent.objects.update_or_create(user_id=request.demo_user_id, purpose=purpose, defaults={"granted": granted, "version": "development-1"})
    record_event(request, "privacy.consent.updated", consent, {"purpose": purpose, "granted": granted, "version": consent.version})
    messages.success(request, "Your privacy preference was saved.")
    return redirect("privacy:center")

def create_request(request):
    if request.method != "POST" or not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}): return redirect("auth_login")
    form = PrivacyRequestForm(request.POST)
    if form.is_valid():
        privacy_request = form.save(commit=False)
        privacy_request.user_id = request.demo_user_id
        privacy_request.save()
        record_event(request, "privacy.request.created", privacy_request, {"request_type": privacy_request.request_type})
        messages.success(request, "Your privacy request was recorded for review.")
    else:
        messages.error(request, "Choose a valid privacy request type.")
    return redirect("privacy:center")

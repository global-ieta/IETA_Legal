from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.services import require_demo_role
from apps.audit.services import record_event
from apps.core.rate_limit import apply_rate_limit_headers, check_request
from apps.consultations.models import Consultation
from integrations.calling.exceptions import CallingIntegrationUnavailable
from integrations.calling.services import get_signaling_provider
from .models import CallSession

def _participant_queryset(request):
    if request.demo_role == "USER":
        return Consultation.objects.filter(user_id=request.demo_user_id)
    return Consultation.objects.filter(advocate__user_id=request.demo_user_id)

def lobby(request, consultation_id, mode):
    if not require_demo_role(request, {"USER", "ADVOCATE"}) or mode not in {CallSession.Modes.AUDIO, CallSession.Modes.VIDEO}:
        return redirect("auth_login")
    consultation = get_object_or_404(_participant_queryset(request).select_related("matter", "user", "advocate__user"), pk=consultation_id, status=Consultation.Status.CONFIRMED)
    session, _ = CallSession.objects.get_or_create(consultation=consultation, mode=mode, defaults={"status": "ready"})
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "start":
            rate_limit = check_request(request, "calls")
            if not rate_limit.allowed:
                messages.error(request, "Call start requests are temporarily limited.")
                record_event(request, "call.rate_limited", session, {"bucket": "calls", "limit": rate_limit.limit})
                return apply_rate_limit_headers(redirect("calling:lobby", consultation_id=consultation.pk, mode=mode), rate_limit)
            provider = get_signaling_provider()
            try:
                signaling_session = provider.create_session(call_id=str(session.pk), mode=mode)
            except CallingIntegrationUnavailable:
                messages.error(request, "Production calling is not configured yet.")
                return redirect("calling:lobby", consultation_id=consultation.pk, mode=mode)
            session.status = "simulated_active"
            session.signaling_provider = "mock-development" if signaling_session.status == "simulated" else "official-signaling"
            session.provider_session_id = signaling_session.session_id
            session.save(update_fields=["status", "signaling_provider", "provider_session_id", "updated_at"])
            record_event(request, "call.started", session, {"mode": mode, "provider": session.signaling_provider, "provider_metadata": signaling_session.metadata, "production_ready": False})
        elif action == "finish":
            if session.provider_session_id:
                try:
                    get_signaling_provider().close_session(session_id=session.provider_session_id)
                except CallingIntegrationUnavailable:
                    messages.error(request, "The configured calling provider is unavailable; the local session was still ended.")
            session.status = "ended"
            session.save(update_fields=["status", "updated_at"])
            record_event(request, "call.ended", session, {"mode": mode})
        return redirect("calling:lobby", consultation_id=consultation.pk, mode=mode)
    return render(request, "portal/call_lobby.html", {"consultation": consultation, "call_session": session, "mode": mode})

def status(request):
    if not require_demo_role(request, {"USER", "ADVOCATE"}):
        return JsonResponse({"error": "Authentication required."}, status=403)
    sessions = CallSession.objects.filter(
        consultation__in=_participant_queryset(request),
        status="simulated_active",
    ).values("id", "mode", "status", "signaling_provider", "updated_at")
    configured = bool(settings.CALLING_API_BASE_URL and settings.CALLING_API_KEY)
    return JsonResponse({
        "audio": "architecture-ready",
        "video": "architecture-ready",
        "production_ready": False,
        "provider_state": "official-configured" if configured else "development-simulation",
        "active_sessions": [
            {
                "id": item["id"],
                "mode": item["mode"],
                "status": item["status"],
                "provider": item["signaling_provider"],
                "updated_at": item["updated_at"].isoformat(),
            }
            for item in sessions
        ],
    })

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.services import require_demo_role
from apps.audit.services import record_event
from apps.core.rate_limit import apply_rate_limit_headers, check_request
from integrations.aura.exceptions import AuraIntegrationUnavailable
from integrations.aura.validators import validate_provider_response, validate_user_message
from .models import AuraConversation, AuraMessage
from .services import get_aura_provider

def workspace(request):
    if not require_demo_role(request, {"USER"}): return redirect("auth_login")
    conversation, _ = AuraConversation.objects.get_or_create(user_id=request.demo_user_id, status=AuraConversation.Status.ACTIVE)
    return render(request, "user/aura_persisted.html", {"conversation": conversation, "messages": conversation.messages.order_by("created_at")})

def message(request):
    if request.method != "POST" or not require_demo_role(request, {"USER"}):
        return JsonResponse({"error": "AURA workspace access required."}, status=403)
    rate_limit = check_request(request, "aura")
    if not rate_limit.allowed:
        record_event(request, "aura.rate_limited", metadata={"bucket": "aura", "limit": rate_limit.limit})
        return apply_rate_limit_headers(JsonResponse({"error": "AURA request limit reached. Please wait before trying again."}, status=429), rate_limit)
    try:
        message = validate_user_message(request.POST.get("message", ""))
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    conversation = get_object_or_404(AuraConversation, pk=request.POST.get("conversation_id"), user_id=request.demo_user_id, status=AuraConversation.Status.ACTIVE) if request.POST.get("conversation_id") else AuraConversation.objects.create(user_id=request.demo_user_id)
    AuraMessage.objects.create(conversation=conversation, role=AuraMessage.Roles.USER, body=message)
    try:
        reply = get_aura_provider().intake_conversation(message)
    except AuraIntegrationUnavailable as exc:
        record_event(request, "aura.unavailable", metadata={"reason": str(exc)})
        return JsonResponse({"error": "AURA is not connected. The official integration contract is still pending."}, status=503)
    try:
        reply = validate_provider_response(reply)
    except ValueError:
        record_event(request, "aura.invalid_response", conversation)
        return JsonResponse({"error": "AURA could not provide a safe response. Please try again later."}, status=502)
    assistant_message = AuraMessage.objects.create(conversation=conversation, role=AuraMessage.Roles.ASSISTANT, body=reply)
    record_event(request, "aura.message", conversation, {"message_length": len(message)})
    return JsonResponse({"reply": assistant_message.body, "conversation_id": conversation.pk})

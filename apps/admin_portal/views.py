from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from apps.accounts.services import require_demo_role
from apps.audit.models import AuditEvent
from apps.audit.services import record_event
from apps.documents.models import PrivateDocument
from apps.privacy.models import PrivacyRequest
from apps.core.integration_readiness import get_integration_readiness

def _require_admin(request):
    return require_demo_role(request, {"ADMIN"})

def documents(request):
    if not _require_admin(request):
        return redirect("auth_login")
    pending = PrivateDocument.objects.select_related("matter", "uploaded_by").filter(status=PrivateDocument.Status.PENDING_REVIEW)
    integration_state = get_integration_readiness()
    return render(request, "admin/document_review.html", {"documents": pending, "pending_count": pending.count(), "scanner_state": integration_state["document_scanning"], "storage_state": integration_state["private_storage"]})

def review_document(request, pk, decision):
    if request.method != "POST" or not _require_admin(request):
        return redirect("auth_login")
    document = get_object_or_404(PrivateDocument, pk=pk, status=PrivateDocument.Status.PENDING_REVIEW)
    if decision == "approve":
        if get_integration_readiness()["document_scanning"]["implementation"] == "contract-pending":
            messages.error(request, "The configured document scanner is not implemented; approval is blocked until its contract is reviewed.")
            return redirect("admin_portal:documents")
        document.status = PrivateDocument.Status.AVAILABLE
        message = "Document approved for authorised matter participants."
        action = "document.approved"
    elif decision == "reject":
        document.status = PrivateDocument.Status.REJECTED
        message = "Document rejected and kept unavailable."
        action = "document.rejected"
    else:
        messages.error(request, "Unsupported document review decision.")
        return redirect("admin_portal:documents")
    document.save(update_fields=["status", "updated_at"])
    record_event(request, action, document)
    messages.success(request, message)
    return redirect("admin_portal:documents")

def audit_log(request):
    if not _require_admin(request):
        return redirect("auth_login")
    action = request.GET.get("action", "")
    request_id = request.GET.get("request_id", "").strip()[:64]
    events = AuditEvent.objects.select_related("actor").order_by("-created_at")
    if action:
        events = events.filter(action=action)
    if request_id:
        events = events.filter(request_id=request_id)
    event_count = events.count()
    paginator = Paginator(events[:100], 25)
    return render(request, "admin/audit_log.html", {
        "events": paginator.get_page(request.GET.get("page")),
        "action_filter": action,
        "request_id_filter": request_id,
        "available_actions": AuditEvent.objects.order_by("action").values_list("action", flat=True).distinct(),
        "event_count": event_count,
    })

def integration_status(request):
    if not _require_admin(request):
        return redirect("auth_login")
    return render(request, "admin/integrations.html", {"integration_report": get_integration_readiness()})

def privacy_requests(request):
    if not _require_admin(request):
        return redirect("auth_login")
    selected_status = request.GET.get("status", "open")
    requests = PrivacyRequest.objects.select_related("user")
    if selected_status == "open":
        requests = requests.exclude(status=PrivacyRequest.Status.COMPLETED)
    elif selected_status in PrivacyRequest.Status.values:
        requests = requests.filter(status=selected_status)
    else:
        selected_status = "open"
        requests = requests.exclude(status=PrivacyRequest.Status.COMPLETED)
    request_items = list(requests)
    now = timezone.now()
    for item in request_items:
        item.age_days = max((now - item.created_at).days, 0)
    return render(request, "admin/privacy_requests.html", {
        "privacy_requests": request_items,
        "selected_status": selected_status,
        "status_choices": PrivacyRequest.Status.choices,
        "request_count": requests.count(),
        "open_count": PrivacyRequest.objects.exclude(status=PrivacyRequest.Status.COMPLETED).count(),
    })

def review_privacy_request(request, pk, decision):
    if request.method != "POST" or not _require_admin(request):
        return redirect("auth_login")
    privacy_request = get_object_or_404(PrivacyRequest, pk=pk)
    statuses = {"review": PrivacyRequest.Status.UNDER_REVIEW, "complete": PrivacyRequest.Status.COMPLETED, "decline": PrivacyRequest.Status.DECLINED}
    if decision not in statuses:
        messages.error(request, "Unsupported privacy request decision.")
        return redirect("admin_portal:privacy_requests")
    allowed_decisions = {
        PrivacyRequest.Status.REQUESTED: {"review", "decline"},
        PrivacyRequest.Status.UNDER_REVIEW: {"complete", "decline"},
    }
    if decision not in allowed_decisions.get(privacy_request.status, set()):
        messages.error(request, "This privacy request is already in a terminal state or cannot take that transition.")
        return redirect("admin_portal:privacy_requests")
    privacy_request.status = statuses[decision]
    privacy_request.save(update_fields=["status", "updated_at"])
    action = "privacy.request.reviewed" if decision == "review" else f"privacy.request.{decision}d"
    record_event(request, action, privacy_request, {"request_type": privacy_request.request_type})
    messages.success(request, "Privacy request status updated.")
    return redirect("admin_portal:privacy_requests")

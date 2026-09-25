from django.shortcuts import redirect, render
from apps.accounts.services import require_demo_role
from apps.intake.models import IntakeRecord
from apps.matters.models import Matter
from apps.consultations.models import Consultation
from apps.advocates.models import AdvocateProfile
from apps.accounts.models import UserProfile
from apps.consultations.models import ConflictCheck
from apps.notifications.models import Notification
from apps.documents.models import PrivateDocument
from apps.privacy.models import PrivacyRequest
from apps.calling.models import CallSession
from apps.core.integration_readiness import get_integration_readiness
def home(request):
    if not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}): return redirect("auth_login")
    display_name = request.session.get("demo_display_name")
    if not display_name:
        display_name = request.user.get_full_name() if request.user.is_authenticated else request.user.get_username()
    context = {"role": request.demo_role, "display_name": display_name}
    if request.demo_role == "USER":
        context.update({"intakes": IntakeRecord.objects.filter(owner_id=request.demo_user_id)[:5], "matters": Matter.objects.filter(owner_id=request.demo_user_id)[:5], "consultations": Consultation.objects.filter(user_id=request.demo_user_id)[:5], "document_count": PrivateDocument.objects.filter(matter__owner_id=request.demo_user_id).count(), "unread_notifications": Notification.objects.filter(recipient_id=request.demo_user_id, read_at__isnull=True).count()})
        template = "user/dashboard_enhanced.html"
    elif request.demo_role == "ADVOCATE":
        context.update({"profile": AdvocateProfile.objects.filter(user_id=request.demo_user_id).first(), "matters": Matter.objects.filter(selected_advocate__user_id=request.demo_user_id)[:5], "consultations": Consultation.objects.filter(advocate__user_id=request.demo_user_id)[:5], "document_count": PrivateDocument.objects.filter(matter__selected_advocate__user_id=request.demo_user_id).count(), "unread_notifications": Notification.objects.filter(recipient_id=request.demo_user_id, read_at__isnull=True).count()})
        template = "advocate/dashboard_enhanced.html"
    else:
        integration_report = get_integration_readiness()
        context.update({
            "user_count": UserProfile.objects.filter(role=UserProfile.Roles.USER).count(),
            "advocate_count": AdvocateProfile.objects.count(),
            "verified_advocate_count": AdvocateProfile.objects.filter(verified=True).count(),
            "matter_count": Matter.objects.count(),
            "pending_conflicts": ConflictCheck.objects.select_related("matter", "advocate").filter(status=ConflictCheck.Status.PENDING)[:10],
            "notification_count": Notification.objects.count(),
            "pending_document_count": PrivateDocument.objects.filter(status=PrivateDocument.Status.PENDING_REVIEW).count(),
            "open_privacy_request_count": PrivacyRequest.objects.exclude(status=PrivacyRequest.Status.COMPLETED).count(),
            "active_call_count": CallSession.objects.filter(status="simulated_active").count(),
            "contract_pending_count": sum(item["implementation"] == "contract-pending" for item in integration_report.values()),
        })
        template = "admin/operations_dashboard_enhanced.html"
    return render(request, template, context)

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.services import require_demo_role
from apps.audit.services import record_event
from apps.messaging.models import Conversation
from apps.notifications.services import create_in_app_notification
from .models import ConflictCheck, Consultation
def list_consultations(request):
    if not require_demo_role(request, {"USER", "ADVOCATE"}): return redirect("auth_login")
    qs = Consultation.objects.filter(user_id=request.demo_user_id) if request.demo_role == "USER" else Consultation.objects.filter(advocate__user_id=request.demo_user_id)
    return render(request, "portal/consultations_workflow_v2.html", {"consultations": qs})

def decide(request, pk, decision):
    if request.method != "POST" or not require_demo_role(request, {"ADVOCATE"}):
        return redirect("auth_login")
    consultation = get_object_or_404(Consultation.objects.select_related("matter", "user", "advocate"), pk=pk, advocate__user_id=request.demo_user_id, status=Consultation.Status.REQUESTED)
    conflict = get_object_or_404(ConflictCheck, matter=consultation.matter, advocate=consultation.advocate)
    if decision == "accept":
        conflict.status = ConflictCheck.Status.CLEAR
        conflict.note = "Conflict review completed for this consultation request."
        conflict.save(update_fields=["status", "note", "updated_at"])
        consultation.status = Consultation.Status.CONFIRMED
        consultation.save(update_fields=["status", "updated_at"])
        Conversation.objects.get_or_create(matter=consultation.matter, user=consultation.user, advocate=consultation.advocate)
        record_event(request, "consultation.accepted", consultation)
        create_in_app_notification(recipient_id=consultation.user_id, kind="consultation", title="Consultation request accepted", body=f"The advocate accepted the request for {consultation.matter.title}. Secure messaging is now available.")
        messages.success(request, "The consultation was accepted and secure messaging is open.")
    elif decision == "decline":
        consultation.status = Consultation.Status.CANCELLED
        consultation.save(update_fields=["status", "updated_at"])
        consultation.matter.selected_advocate = None
        consultation.matter.status = "OPEN"
        consultation.matter.save(update_fields=["selected_advocate", "status", "updated_at"])
        record_event(request, "consultation.declined", consultation)
        create_in_app_notification(recipient_id=consultation.user_id, kind="consultation", body=f"The consultation request for {consultation.matter.title} was declined.", title="Consultation request declined")
        messages.info(request, "The consultation request was declined.")
    return redirect("consultations:list")

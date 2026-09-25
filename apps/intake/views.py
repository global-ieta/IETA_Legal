from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.services import require_demo_role
from apps.accounts.models import UserProfile
from apps.audit.services import record_event
from .forms import IntakeForm
from .models import IntakeRecord
from apps.matters.models import Matter

def start(request):
    if not require_demo_role(request, {"USER"}):
        return redirect("auth_login")
    if request.method == "POST":
        form = IntakeForm(request.POST)
        if form.is_valid():
            intake = form.save(commit=False)
            intake.owner_id = request.demo_user_id
            intake.matter = Matter.objects.create(owner_id=request.demo_user_id, title=intake.title, summary=intake.facts, status=Matter.Status.OPEN)
            intake.save()
            messages.success(request, "Your factual intake draft has been saved.")
            return redirect("intake:review", pk=intake.pk)
    else:
        form = IntakeForm()
    return render(request, "user/intake_form.html", {"form": form})

def _owned_intake(request, pk):
    return get_object_or_404(IntakeRecord.objects.select_related("matter"), pk=pk, owner_id=request.demo_user_id)

def edit(request, pk):
    if not require_demo_role(request, {"USER"}):
        return redirect("auth_login")
    intake = _owned_intake(request, pk)
    if request.method == "POST":
        form = IntakeForm(request.POST, instance=intake)
        if form.is_valid():
            updated = form.save()
            if updated.matter:
                updated.matter.title = updated.title
                updated.matter.summary = updated.facts
                updated.matter.save(update_fields=["title", "summary", "updated_at"])
            return redirect("intake:review", pk=pk)
    else:
        form = IntakeForm(instance=intake)
    return render(request, "user/intake_form.html", {"form": form, "intake": intake, "editing": True})

def review(request, pk):
    if not require_demo_role(request, {"USER"}):
        return redirect("auth_login")
    intake = _owned_intake(request, pk)
    return render(request, "user/intake_review.html", {"intake": intake})

def confirm(request, pk):
    if request.method != "POST" or not require_demo_role(request, {"USER"}):
        return redirect("auth_login")
    intake = _owned_intake(request, pk)
    intake.status = IntakeRecord.Status.CONFIRMED
    intake.save(update_fields=["status", "updated_at"])
    record_event(request, "intake.confirmed", intake, {"matter_id": intake.matter_id})
    return redirect("matters:detail", pk=intake.matter_id)

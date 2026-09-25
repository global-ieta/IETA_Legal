from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.services import require_demo_role
from apps.consultations.models import ConflictCheck, Consultation
from apps.matters.models import Matter
from .models import AdvocateProfile

def directory(request):
    advocates = AdvocateProfile.objects.filter(verified=True)
    area = request.GET.get("practice_area", "").strip()
    mode = request.GET.get("mode", "").strip()
    if area:
        advocates = [a for a in advocates if area.lower() in [x.lower() for x in a.practice_areas]]
    if mode:
        advocates = [a for a in advocates if mode.lower() in [x.lower() for x in a.consultation_modes]]
    return render(request, "public/advocates.html", {"advocates": advocates, "selected_area": area, "selected_mode": mode})

def profile(request, pk):
    advocate = get_object_or_404(AdvocateProfile, pk=pk, verified=True)
    matters = Matter.objects.filter(owner_id=request.demo_user_id, status__in=[Matter.Status.OPEN, Matter.Status.CONSULTATION]) if require_demo_role(request, {"USER"}) else []
    return render(request, "public/advocate_profile_request.html", {"advocate": advocate, "matters": matters})

def request_consultation(request, pk):
    if request.method != "POST" or not require_demo_role(request, {"USER"}):
        return redirect("auth_login")
    advocate = get_object_or_404(AdvocateProfile, pk=pk, verified=True)
    matter = get_object_or_404(Matter, pk=request.POST.get("matter_id"), owner_id=request.demo_user_id)
    if ConflictCheck.objects.filter(matter=matter, advocate=advocate, status=ConflictCheck.Status.FLAGGED).exists():
        messages.error(request, "This request requires a conflict review before it can continue.")
        return redirect("advocates:profile", pk=pk)
    ConflictCheck.objects.get_or_create(matter=matter, advocate=advocate, defaults={"note": "Awaiting advocate review; no external conflict service is connected."})
    Consultation.objects.get_or_create(matter=matter, user_id=request.demo_user_id, advocate=advocate, defaults={"mode": request.POST.get("mode", "video")})
    matter.selected_advocate = advocate
    matter.status = Matter.Status.CONSULTATION
    matter.save(update_fields=["selected_advocate", "status", "updated_at"])
    messages.success(request, "Your advocate choice was recorded. The conflict check is awaiting review.")
    return redirect("consultations:list")

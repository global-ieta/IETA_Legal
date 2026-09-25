from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.services import require_demo_role
from .models import Matter

def list_matters(request):
    if not require_demo_role(request, {"USER", "ADVOCATE"}):
        return redirect("auth_login")
    matters = Matter.objects.filter(owner_id=request.demo_user_id) if request.demo_role == "USER" else Matter.objects.filter(selected_advocate__user_id=request.demo_user_id)
    return render(request, "portal/matters_enhanced.html", {"matters": matters})

def detail(request, pk):
    if not require_demo_role(request, {"USER", "ADVOCATE"}):
        return redirect("auth_login")
    matters = Matter.objects.filter(owner_id=request.demo_user_id) if request.demo_role == "USER" else Matter.objects.filter(selected_advocate__user_id=request.demo_user_id)
    matter = get_object_or_404(matters.select_related("owner", "selected_advocate", "intake"), pk=pk)
    return render(request, "portal/matter_detail.html", {"matter": matter, "documents": matter.documents.all(), "consultations": matter.consultations.select_related("advocate"), "conversations": matter.conversations.all()})

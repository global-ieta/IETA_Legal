from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from apps.accounts.services import require_demo_role
from apps.audit.services import record_event
from .services import get_notification_delivery_policy
from .models import Notification

def inbox(request):
    if not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}):
        return redirect("auth_login")
    notifications = Notification.objects.filter(recipient_id=request.demo_user_id)[:30]
    return render(request, "portal/notifications_center.html", {"notifications": notifications, "unread_count": Notification.objects.filter(recipient_id=request.demo_user_id, read_at__isnull=True).count(), "delivery_policy": get_notification_delivery_policy(request.demo_user_id)})

def mark_read(request, pk):
    if request.method != "POST" or not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}):
        return redirect("auth_login")
    notification = get_object_or_404(Notification, pk=pk, recipient_id=request.demo_user_id)
    notification.read_at = timezone.now()
    notification.save(update_fields=["read_at", "updated_at"])
    record_event(request, "notification.read", notification)
    return redirect("notifications:inbox")

def mark_all_read(request):
    if request.method != "POST" or not require_demo_role(request, {"USER", "ADVOCATE", "ADMIN"}):
        return redirect("auth_login")
    unread = Notification.objects.filter(recipient_id=request.demo_user_id, read_at__isnull=True)
    updated_count = unread.update(read_at=timezone.now())
    record_event(request, "notifications.read_all", metadata={"count": updated_count})
    messages.success(request, "Notifications marked as read.")
    return redirect("notifications:inbox")

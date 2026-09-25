from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from apps.accounts.services import require_demo_role
from apps.audit.services import record_event
from apps.core.rate_limit import apply_rate_limit_headers, check_request
from apps.notifications.services import create_in_app_notification
from .models import Conversation, Message
def inbox(request):
    if not require_demo_role(request, {"USER", "ADVOCATE"}): return redirect("auth_login")
    qs = Conversation.objects.select_related("matter", "advocate__user").filter(user_id=request.demo_user_id) if request.demo_role == "USER" else Conversation.objects.select_related("matter", "user").filter(advocate__user_id=request.demo_user_id)
    return render(request, "portal/messages_inbox.html", {"conversations": qs})

def detail(request, pk):
    if not require_demo_role(request, {"USER", "ADVOCATE"}):
        return redirect("auth_login")
    scope = Q(user_id=request.demo_user_id) if request.demo_role == "USER" else Q(advocate__user_id=request.demo_user_id)
    conversation = get_object_or_404(Conversation.objects.select_related("matter", "user", "advocate__user").filter(scope), pk=pk)
    if request.method == "POST":
        rate_limit = check_request(request, "messages")
        if not rate_limit.allowed:
            messages.error(request, "Message sending is temporarily limited. Please wait before trying again.")
            record_event(request, "message.rate_limited", conversation, {"bucket": "messages", "limit": rate_limit.limit})
            response = render(request, "portal/message_detail.html", {"conversation": conversation, "messages_list": conversation.messages.select_related("sender")}, status=429)
            return apply_rate_limit_headers(response, rate_limit)
        body = request.POST.get("body", "").strip()
        if not body or len(body) > 5000:
            messages.error(request, "Messages must contain between 1 and 5,000 characters.")
        else:
            Message.objects.create(conversation=conversation, sender_id=request.demo_user_id, body=body)
            record_event(request, "message.sent", conversation, {"body_length": len(body)})
            recipient_id = conversation.advocate.user_id if request.demo_role == "USER" else conversation.user_id
            create_in_app_notification(recipient_id=recipient_id, kind="message", title="New secure message", body=f"A new message is available in {conversation.matter.title}.")
            return redirect("messaging:detail", pk=pk)
    return render(request, "portal/message_detail.html", {"conversation": conversation, "messages_list": conversation.messages.select_related("sender")})

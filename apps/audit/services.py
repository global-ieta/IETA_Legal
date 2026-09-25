from .models import AuditEvent

def record_event(request, action, obj=None, metadata=None):
    """Persist a minimal event; replace or fan out to a production audit sink later."""
    return AuditEvent.objects.create(
        actor_id=getattr(request, "demo_user_id", None),
        action=action,
        object_type=obj.__class__.__name__ if obj is not None else "",
        object_id=str(getattr(obj, "pk", "")) if obj is not None else "",
        request_id=getattr(request, "request_id", ""),
        metadata=metadata or {},
    )

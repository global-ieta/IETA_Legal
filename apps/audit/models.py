from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel
class AuditEvent(TimestampedModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    request_id = models.CharField(max_length=64, blank=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"], name="audit_created_idx"),
            models.Index(fields=["action", "-created_at"], name="audit_action_created_idx"),
            models.Index(fields=["request_id"], name="audit_request_idx"),
        ]

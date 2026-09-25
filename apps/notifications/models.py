from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel

class Notification(TimestampedModel):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    kind = models.CharField(max_length=40, default="info")
    title = models.CharField(max_length=180)
    body = models.TextField()
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

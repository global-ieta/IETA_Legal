from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel

class Matter(TimestampedModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        OPEN = "OPEN", "Open"
        CONSULTATION = "CONSULTATION", "Consultation"
        CLOSED = "CLOSED", "Closed"
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="matters")
    title = models.CharField(max_length=180)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    selected_advocate = models.ForeignKey("advocates.AdvocateProfile", null=True, blank=True, on_delete=models.SET_NULL, related_name="matters")

class MatterAccess(models.Model):
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name="access_grants")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=160)
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["matter", "user"], name="unique_matter_access")]

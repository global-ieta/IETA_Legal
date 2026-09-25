from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel
class Consultation(TimestampedModel):
    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        CONFIRMED = "CONFIRMED", "Confirmed"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
    matter = models.ForeignKey("matters.Matter", on_delete=models.CASCADE, related_name="consultations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consultations")
    advocate = models.ForeignKey("advocates.AdvocateProfile", on_delete=models.CASCADE, related_name="consultations")
    scheduled_for = models.DateTimeField(null=True, blank=True)
    mode = models.CharField(max_length=20, default="video")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)

class ConflictCheck(TimestampedModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Awaiting advocate review"
        CLEAR = "CLEAR", "No conflict recorded"
        FLAGGED = "FLAGGED", "Requires review"
    matter = models.ForeignKey("matters.Matter", on_delete=models.CASCADE, related_name="conflict_checks")
    advocate = models.ForeignKey("advocates.AdvocateProfile", on_delete=models.CASCADE, related_name="conflict_checks")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    note = models.CharField(max_length=240, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["matter", "advocate"], name="unique_matter_advocate_conflict")]

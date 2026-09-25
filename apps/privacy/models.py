from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel
class Consent(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consents")
    purpose = models.CharField(max_length=120)
    granted = models.BooleanField(default=False)
    version = models.CharField(max_length=30)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "purpose"], name="unique_user_consent_purpose")]

class PrivacyRequest(TimestampedModel):
    class RequestTypes(models.TextChoices):
        ACCESS = "ACCESS", "Access request"
        DELETION = "DELETION", "Deletion request"
    class Status(models.TextChoices):
        REQUESTED = "REQUESTED", "Requested"
        UNDER_REVIEW = "UNDER_REVIEW", "Under review"
        COMPLETED = "COMPLETED", "Completed"
        DECLINED = "DECLINED", "Declined"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="privacy_requests")
    request_type = models.CharField(max_length=20, choices=RequestTypes.choices)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)

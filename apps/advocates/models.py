from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel

class AdvocateProfile(TimestampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="advocate_profile")
    display_name = models.CharField(max_length=160)
    practice_areas = models.JSONField(default=list)
    jurisdictions = models.JSONField(default=list)
    languages = models.JSONField(default=list)
    consultation_modes = models.JSONField(default=list)
    bio = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    available = models.BooleanField(default=False)

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name

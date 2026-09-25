from django.db import models
from apps.core.models import TimestampedModel
class CallSession(TimestampedModel):
    class Modes(models.TextChoices):
        AUDIO = "audio", "Audio"
        VIDEO = "video", "Video"
    consultation = models.ForeignKey("consultations.Consultation", on_delete=models.CASCADE, related_name="calls")
    mode = models.CharField(max_length=10, choices=Modes.choices)
    status = models.CharField(max_length=20, default="not_started")
    signaling_provider = models.CharField(max_length=80, default="awaiting-owner-integration")
    provider_session_id = models.CharField(max_length=200, blank=True)

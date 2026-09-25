from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel

class IntakeRecord(TimestampedModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        REVIEW = "REVIEW", "Ready for review"
        CONFIRMED = "CONFIRMED", "Confirmed"
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="intakes")
    matter = models.OneToOneField("matters.Matter", null=True, blank=True, on_delete=models.SET_NULL, related_name="intake")
    title = models.CharField(max_length=180, default="Untitled situation")
    facts = models.TextField(blank=True)
    incident_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=180, blank=True)
    involved_parties = models.TextField(blank=True)
    timeline = models.TextField(blank=True)
    questions = models.TextField(blank=True)
    missing_information = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

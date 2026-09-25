from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel

class AuraConversation(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CLOSED = "CLOSED", "Closed"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="aura_conversations")
    title = models.CharField(max_length=180, default="AURA factual intake")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

class AuraMessage(TimestampedModel):
    class Roles(models.TextChoices):
        USER = "USER", "User"
        ASSISTANT = "ASSISTANT", "AURA"
    conversation = models.ForeignKey(AuraConversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=Roles.choices)
    body = models.TextField()
    metadata = models.JSONField(default=dict)

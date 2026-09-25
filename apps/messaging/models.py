from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel
class Conversation(TimestampedModel):
    matter = models.ForeignKey("matters.Matter", on_delete=models.CASCADE, related_name="conversations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_user")
    advocate = models.ForeignKey("advocates.AdvocateProfile", on_delete=models.CASCADE, related_name="conversations")
class Message(TimestampedModel):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()

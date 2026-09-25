import uuid
from django.conf import settings
from django.db import models
from apps.core.models import TimestampedModel
from .storage import PrivateDocumentStorage

private_storage = PrivateDocumentStorage()

def private_document_upload_path(instance, filename):
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else "bin"
    return f"matter-{instance.matter_id}/{uuid.uuid4().hex}.{extension}"

class PrivateDocument(TimestampedModel):
    class Status(models.TextChoices):
        PENDING_REVIEW = "PENDING_REVIEW", "Pending security review"
        AVAILABLE = "AVAILABLE", "Available"
        REJECTED = "REJECTED", "Rejected"
    matter = models.ForeignKey("matters.Matter", on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="uploaded_documents")
    file = models.FileField(upload_to=private_document_upload_path, storage=private_storage)
    original_name = models.CharField(max_length=255)
    content_type = models.CharField(max_length=120, blank=True)
    size = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING_REVIEW)

    class Meta:
        ordering = ["-created_at"]

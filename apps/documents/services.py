from pathlib import Path
from django.core.exceptions import ValidationError
from .models import PrivateDocument

MAX_UPLOAD_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".png", ".jpg", ".jpeg"}
ALLOWED_CONTENT_TYPES = {"application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "image/png", "image/jpeg", ""}

def validate_private_upload(upload):
    extension = Path(upload.name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError("This file type is not accepted for private document upload.")
    if upload.size > MAX_UPLOAD_SIZE:
        raise ValidationError("Private documents must be 10 MB or smaller.")
    if getattr(upload, "content_type", "") not in ALLOWED_CONTENT_TYPES:
        raise ValidationError("The reported file type is not accepted.")

def can_access_document(document, user_id, role):
    if role == "USER":
        return document.matter.owner_id == user_id
    if role == "ADVOCATE":
        return document.matter.selected_advocate_id and document.matter.selected_advocate.user_id == user_id
    return role == "ADMIN"

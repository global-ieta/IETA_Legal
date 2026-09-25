from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    class Roles(models.TextChoices):
        USER = "USER", "User"
        ADVOCATE = "ADVOCATE", "Advocate"
        ADMIN = "ADMIN", "Admin"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ieta_profile")
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.USER)
    display_name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.display_name} ({self.role})"

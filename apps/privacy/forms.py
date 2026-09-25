from django import forms
from .models import PrivacyRequest

class PrivacyRequestForm(forms.ModelForm):
    class Meta:
        model = PrivacyRequest
        fields = ["request_type", "note"]
        widgets = {"note": forms.Textarea(attrs={"rows": 3, "placeholder": "Optional context for the privacy team"})}

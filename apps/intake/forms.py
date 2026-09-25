from django import forms
from .models import IntakeRecord

class IntakeForm(forms.ModelForm):
    class Meta:
        model = IntakeRecord
        fields = ["title", "facts", "incident_date", "location", "involved_parties", "timeline", "questions"]
        widgets = {"incident_date": forms.DateInput(attrs={"type": "date"}), "facts": forms.Textarea(attrs={"rows": 5}), "involved_parties": forms.Textarea(attrs={"rows": 3}), "timeline": forms.Textarea(attrs={"rows": 4}), "questions": forms.Textarea(attrs={"rows": 3})}

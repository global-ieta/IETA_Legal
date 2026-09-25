from django import forms
from .services import validate_private_upload

class PrivateDocumentForm(forms.Form):
    file = forms.FileField(label="Private document")

    def clean_file(self):
        upload = self.cleaned_data["file"]
        validate_private_upload(upload)
        return upload

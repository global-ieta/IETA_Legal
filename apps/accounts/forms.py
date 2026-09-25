from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class LoginForm(forms.Form):
    identifier = forms.CharField(label="Login ID or email", max_length=254)
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput)


class AccountRegistrationForm(forms.Form):
    login_id = forms.CharField(label="Login ID", max_length=150)
    email = forms.EmailField(label="Email address")
    display_name = forms.CharField(label="Full name", max_length=120)
    password = forms.CharField(label="Create password", strip=False, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label="Confirm password", strip=False, widget=forms.PasswordInput)

    def clean_login_id(self):
        value = self.cleaned_data["login_id"].strip()
        if get_user_model().objects.filter(username__iexact=value).exists():
            raise forms.ValidationError("That login ID is already in use.")
        return value

    def clean_email(self):
        value = self.cleaned_data["email"].strip().lower()
        if get_user_model().objects.filter(email__iexact=value).exists():
            raise forms.ValidationError("That email address is already in use.")
        return value

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        confirmation = cleaned.get("password_confirmation")
        if password and confirmation and password != confirmation:
            self.add_error("password_confirmation", "Passwords do not match.")
        if password:
            try:
                validate_password(password)
            except forms.ValidationError as exc:
                self.add_error("password", exc)
        return cleaned


class AdvocateRegistrationForm(AccountRegistrationForm):
    practice_areas = forms.CharField(label="Practice areas", help_text="Separate areas with commas.")
    jurisdictions = forms.CharField(label="Jurisdictions", help_text="Separate jurisdictions with commas.")
    languages = forms.CharField(label="Languages", help_text="Separate languages with commas.")
    consultation_modes = forms.CharField(label="Consultation modes", help_text="For example: Audio, Video.")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["display_name"]
        labels = {"display_name": "Display name"}

class AdvocateProfileSettingsForm(forms.Form):
    display_name = forms.CharField(max_length=160, label="Professional display name")
    bio = forms.CharField(max_length=2000, required=False, widget=forms.Textarea(attrs={"rows": 4}))
    available = forms.BooleanField(required=False, label="Show development availability")

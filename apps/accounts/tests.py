from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import UserProfile
from apps.advocates.models import AdvocateProfile

class DemoModeTests(TestCase):
    @override_settings(DEMO_MODE=True)
    def test_role_entry_creates_user_session(self):
        response = self.client.post(reverse("accounts:entry"), {"role": "USER"})
        self.assertRedirects(response, reverse("portal:home"))
        self.assertEqual(self.client.session["demo_role"], "USER")

    @override_settings(DEMO_MODE=False)
    def test_role_entry_is_disabled(self):
        self.assertEqual(self.client.get(reverse("accounts:entry")).status_code, 404)

    @override_settings(DEMO_MODE=True)
    def test_user_can_update_development_profile(self):
        self.client.post(reverse("accounts:entry"), {"role": "USER"})
        response = self.client.post(reverse("accounts_profile:profile"), {"display_name": "Updated Development User"})
        self.assertRedirects(response, reverse("accounts_profile:profile"))
        self.assertEqual(self.client.session["demo_display_name"], "Updated Development User")

    @override_settings(DEMO_MODE=True)
    def test_advocate_profile_settings_stay_separate(self):
        self.client.post(reverse("accounts:entry"), {"role": "ADVOCATE"})
        response = self.client.post(reverse("accounts_profile:profile"), {"display_name": "Development Counsel", "bio": "Updated development biography", "available": "on"})
        self.assertRedirects(response, reverse("accounts_profile:profile"))
        from apps.advocates.models import AdvocateProfile
        advocate = AdvocateProfile.objects.get(user__username="demo_advocate")
        self.assertEqual(advocate.display_name, "Development Counsel")
        self.assertEqual(advocate.bio, "Updated development biography")

    def test_login_page_separates_user_and_advocate_workspaces(self):
        response = self.client.get(reverse("auth_login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in as a")
        self.assertContains(response, "Sign in as an")
        self.assertContains(response, 'value="USER"')
        self.assertContains(response, 'value="ADVOCATE"')
        self.assertNotContains(response, "Development mode")

    def test_login_requires_the_selected_workspace_to_match_account_role(self):
        user = get_user_model().objects.create_user(username="workspace_user", password="SecurePass123!")
        UserProfile.objects.create(user=user, role=UserProfile.Roles.USER, display_name="Workspace User")

        response = self.client.post(reverse("auth_login"), {
            "login_role": UserProfile.Roles.ADVOCATE,
            "advocate-identifier": "workspace_user",
            "advocate-password": "SecurePass123!",
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "different workspace")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_user_registration_hashes_password_and_enters_user_portal(self):
        response = self.client.post(reverse("auth_register"), {
            "login_id": "new_user",
            "email": "new.user@example.com",
            "display_name": "New User",
            "password": "SecurePass123!",
            "password_confirmation": "SecurePass123!",
        })

        self.assertRedirects(response, reverse("portal:home"))
        user = get_user_model().objects.get(username="new_user")
        self.assertTrue(user.check_password("SecurePass123!"))
        self.assertNotEqual(user.password, "SecurePass123!")
        self.assertEqual(user.ieta_profile.role, UserProfile.Roles.USER)
        self.assertTrue(self.client.session.get("_auth_user_id"))

    def test_login_accepts_email_and_rejects_invalid_password(self):
        user = get_user_model().objects.create_user(username="login_user", email="login@example.com", password="SecurePass123!")
        UserProfile.objects.create(user=user, role=UserProfile.Roles.USER, display_name="Login User")

        invalid = self.client.post(reverse("auth_login"), {"identifier": "login@example.com", "password": "wrong-password"})
        valid = self.client.post(reverse("auth_login"), {"identifier": "login@example.com", "password": "SecurePass123!"})

        self.assertEqual(invalid.status_code, 200)
        self.assertContains(invalid, "could not be verified")
        self.assertRedirects(valid, reverse("portal:home"))

    @override_settings(AUTH_PROVIDER="global_ieta")
    def test_official_identity_provider_fails_closed_without_contract(self):
        response = self.client.post(reverse("auth_login"), {"identifier": "member@example.com", "password": "SecurePass123!"})

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "temporarily unavailable", status_code=503)
        self.assertNotIn("_auth_user_id", self.client.session)

    @override_settings(AUTH_PROVIDER="global_ieta")
    def test_registration_fails_closed_without_official_identity_contract(self):
        response = self.client.post(reverse("auth_register"), {})

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "temporarily unavailable", status_code=503)
        self.assertFalse(get_user_model().objects.filter(username="new_user").exists())

    def test_advocate_registration_creates_professional_profile(self):
        response = self.client.post(reverse("auth_register_advocate"), {
            "login_id": "new_advocate",
            "email": "advocate@example.com",
            "display_name": "New Advocate",
            "password": "SecurePass123!",
            "password_confirmation": "SecurePass123!",
            "practice_areas": "Civil, Employment",
            "jurisdictions": "Delhi",
            "languages": "English, Hindi",
            "consultation_modes": "Audio, Video",
        })

        self.assertRedirects(response, reverse("portal:home"))
        advocate = AdvocateProfile.objects.get(user__username="new_advocate")
        self.assertEqual(advocate.practice_areas, ["Civil", "Employment"])
        self.assertEqual(advocate.user.ieta_profile.role, UserProfile.Roles.ADVOCATE)

    def test_logout_ends_authenticated_session(self):
        user = get_user_model().objects.create_user(username="logout_user", password="SecurePass123!")
        UserProfile.objects.create(user=user, role=UserProfile.Roles.USER, display_name="Logout User")
        self.client.post(reverse("auth_login"), {"identifier": "logout_user", "password": "SecurePass123!"})

        response = self.client.post(reverse("auth_logout"))

        self.assertRedirects(response, reverse("public:home"))
        self.assertNotIn("_auth_user_id", self.client.session)

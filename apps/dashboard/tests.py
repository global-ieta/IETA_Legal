from django.test import TestCase
from django.urls import reverse

class PortalBoundaryTests(TestCase):
    def test_portal_requires_demo_role(self):
        response = self.client.get(reverse("portal:home"))
        self.assertRedirects(response, reverse("auth_login"))

    def test_admin_endpoint_does_not_accept_demo_role_as_django_auth(self):
        session = self.client.session
        session["demo_role"] = "USER"
        session.save()
        response = self.client.get("/admin/")
        self.assertIn(response.status_code, {302, 403})

    def test_admin_dashboard_shows_operational_attention_summary(self):
        session = self.client.session
        session["demo_role"] = "ADMIN"
        session["demo_user_id"] = 999
        session["demo_display_name"] = "Development Admin"
        session.save()

        response = self.client.get(reverse("portal:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "DOCUMENT REVIEW")
        self.assertContains(response, "PRIVACY QUEUE")
        self.assertContains(response, "ACTIVE CALLS")
        self.assertContains(response, "INTEGRATION CONTRACTS")

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from apps.advocates.models import AdvocateProfile
from apps.consultations.models import Consultation
from apps.matters.models import Matter
from .models import CallSession

class CallingAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username="call_user")
        advocate_user = User.objects.create(username="call_advocate")
        self.advocate = AdvocateProfile.objects.create(user=advocate_user, display_name="Call Advocate", verified=True)
        matter = Matter.objects.create(owner=self.user, title="Call matter", selected_advocate=self.advocate, status=Matter.Status.CONSULTATION)
        self.consultation = Consultation.objects.create(matter=matter, user=self.user, advocate=self.advocate, status=Consultation.Status.CONFIRMED, mode="video")

    def _session(self, role, user_id):
        session = self.client.session
        session["demo_role"] = role
        session["demo_user_id"] = user_id
        session.save()

    def test_related_user_can_start_and_end_simulated_call(self):
        self._session("USER", self.user.pk)
        url = reverse("calling:lobby", args=[self.consultation.pk, "video"])
        response = self.client.post(url, {"action": "start"})
        self.assertRedirects(response, url)
        call = CallSession.objects.get(consultation=self.consultation)
        self.assertEqual(call.status, "simulated_active")
        self.assertEqual(call.signaling_provider, "mock-development")
        self.assertTrue(call.provider_session_id.startswith("dev-"))
        self.client.post(url, {"action": "finish"})
        call.refresh_from_db()
        self.assertEqual(call.status, "ended")

    def test_unrelated_user_cannot_open_call_lobby(self):
        other = get_user_model().objects.create(username="unrelated_call_user")
        self._session("USER", other.pk)
        response = self.client.get(reverse("calling:lobby", args=[self.consultation.pk, "video"]))
        self.assertEqual(response.status_code, 404)

    def test_status_is_participant_scoped(self):
        self._session("USER", self.user.pk)
        self.client.post(reverse("calling:lobby", args=[self.consultation.pk, "video"]), {"action": "start"})

        response = self.client.get(reverse("calling:status"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["provider_state"], "development-simulation")
        self.assertEqual(len(response.json()["active_sessions"]), 1)
        self.assertEqual(response.json()["active_sessions"][0]["provider"], "mock-development")

    @override_settings(CALLING_API_BASE_URL="https://calling.example", CALLING_API_KEY="test-key")
    def test_configured_provider_fails_closed_without_creating_active_session(self):
        self._session("USER", self.user.pk)
        url = reverse("calling:lobby", args=[self.consultation.pk, "video"])

        response = self.client.post(url, {"action": "start"}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Production calling is not configured yet.")
        self.assertFalse(CallSession.objects.filter(status="simulated_active").exists())

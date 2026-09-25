from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.advocates.models import AdvocateProfile
from apps.matters.models import Matter
from .models import ConflictCheck, Consultation

class ConsultationDecisionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username="consult_user")
        advocate_user = User.objects.create(username="consult_advocate")
        self.advocate = AdvocateProfile.objects.create(user=advocate_user, display_name="Development Advocate", verified=True)
        self.matter = Matter.objects.create(owner=self.user, title="Consultation matter")
        self.consultation = Consultation.objects.create(matter=self.matter, user=self.user, advocate=self.advocate)
        self.conflict = ConflictCheck.objects.create(matter=self.matter, advocate=self.advocate)

    def test_only_related_advocate_can_accept(self):
        session = self.client.session
        session["demo_role"] = "ADVOCATE"
        session["demo_user_id"] = self.advocate.user_id
        session.save()
        response = self.client.post(reverse("consultations:decide", args=[self.consultation.pk, "accept"]))
        self.assertRedirects(response, reverse("consultations:list"))
        self.consultation.refresh_from_db()
        self.assertEqual(self.consultation.status, Consultation.Status.CONFIRMED)
        self.conflict.refresh_from_db()
        self.assertEqual(self.conflict.status, ConflictCheck.Status.CLEAR)

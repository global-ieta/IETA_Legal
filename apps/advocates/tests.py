from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import AdvocateProfile
from apps.intake.models import IntakeRecord
from apps.matters.models import Matter
from apps.consultations.models import Consultation, ConflictCheck

@override_settings(DEMO_MODE=True)
class AdvocateSelectionFlowTests(TestCase):
    def test_user_can_record_choice_after_factual_intake(self):
        self.client.post(reverse("accounts:entry"), {"role": "ADVOCATE"})
        advocate = AdvocateProfile.objects.get(user__username="demo_advocate")
        self.client.post(reverse("accounts:exit"))
        self.client.post(reverse("accounts:entry"), {"role": "USER"})
        self.client.post(reverse("intake:start"), {"title": "Development matter", "facts": "Facts supplied by the development user.", "location": "Development dataset"})
        intake = IntakeRecord.objects.get(owner__username="demo_user")
        response = self.client.post(reverse("advocates:request_consultation", args=[advocate.pk]), {"matter_id": intake.matter_id, "mode": "video"})
        self.assertRedirects(response, reverse("consultations:list"))
        self.assertTrue(Consultation.objects.filter(matter=intake.matter, advocate=advocate).exists())
        self.assertTrue(ConflictCheck.objects.filter(matter=intake.matter, advocate=advocate, status="PENDING").exists())

    def test_user_cannot_submit_someone_elses_matter(self):
        self.client.post(reverse("accounts:entry"), {"role": "ADVOCATE"})
        advocate = AdvocateProfile.objects.get(user__username="demo_advocate")
        self.client.post(reverse("accounts:exit"))
        self.client.post(reverse("accounts:entry"), {"role": "USER"})
        other_user = get_user_model().objects.create(username="other_user")
        other_matter = Matter.objects.create(owner=other_user, title="Not accessible")
        response = self.client.post(reverse("advocates:request_consultation", args=[advocate.pk]), {"matter_id": other_matter.pk})
        self.assertEqual(response.status_code, 404)

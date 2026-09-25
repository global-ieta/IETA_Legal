from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.audit.models import AuditEvent
from .models import IntakeRecord

class IntakeReviewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="intake_user")
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.user.pk
        session.save()

    def test_user_can_review_edit_and_confirm_intake(self):
        response = self.client.post(reverse("intake:start"), {"title": "Reviewable intake", "facts": "Facts as recorded by the user.", "location": "Development dataset"})
        intake = IntakeRecord.objects.get(owner=self.user)
        self.assertRedirects(response, reverse("intake:review", args=[intake.pk]))
        self.assertEqual(self.client.get(reverse("intake:review", args=[intake.pk])).status_code, 200)
        self.client.post(reverse("intake:edit", args=[intake.pk]), {"title": "Updated intake", "facts": "Updated factual record.", "location": "Updated location"})
        response = self.client.post(reverse("intake:confirm", args=[intake.pk]))
        self.assertRedirects(response, reverse("matters:detail", args=[intake.matter_id]))
        intake.refresh_from_db()
        self.assertEqual(intake.status, IntakeRecord.Status.CONFIRMED)
        self.assertTrue(AuditEvent.objects.filter(action="intake.confirmed").exists())

    def test_other_user_cannot_review_intake(self):
        self.client.post(reverse("intake:start"), {"title": "Private intake", "facts": "Private factual record."})
        intake = IntakeRecord.objects.get(owner=self.user)
        other = get_user_model().objects.create(username="other_intake_user")
        session = self.client.session
        session["demo_user_id"] = other.pk
        session.save()
        self.assertEqual(self.client.get(reverse("intake:review", args=[intake.pk])).status_code, 404)

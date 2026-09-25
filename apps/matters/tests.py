from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Matter
from .services import user_can_access_matter

class MatterAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner = User.objects.create(username="owner")
        self.other = User.objects.create(username="other")
        self.matter = Matter.objects.create(owner=self.owner, title="Private matter")

    def test_other_user_cannot_access_matter(self):
        self.assertTrue(user_can_access_matter(self.owner.pk, self.matter))
        self.assertFalse(user_can_access_matter(self.other.pk, self.matter))

    def test_owner_can_open_matter_detail(self):
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.owner.pk
        session.save()
        response = self.client.get(reverse("matters:detail", args=[self.matter.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Private matter")

    def test_unrelated_user_cannot_open_matter_detail(self):
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.other.pk
        session.save()
        response = self.client.get(reverse("matters:detail", args=[self.matter.pk]))
        self.assertEqual(response.status_code, 404)

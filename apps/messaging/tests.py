from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from apps.advocates.models import AdvocateProfile
from apps.consultations.models import Consultation
from apps.matters.models import Matter
from .models import Conversation, Message

class MessagingBoundaryTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username="message_user")
        self.other_user = User.objects.create(username="other_user")
        advocate_user = User.objects.create(username="message_advocate")
        self.advocate = AdvocateProfile.objects.create(user=advocate_user, display_name="Development Advocate", verified=True)
        self.matter = Matter.objects.create(owner=self.user, title="Scoped matter")
        self.conversation = Conversation.objects.create(matter=self.matter, user=self.user, advocate=self.advocate)

    def test_unrelated_user_cannot_open_conversation(self):
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.other_user.pk
        session.save()
        response = self.client.get(reverse("messaging:detail", args=[self.conversation.pk]))
        self.assertEqual(response.status_code, 404)

    def test_authorized_user_can_send_message(self):
        session = self.client.session
        session["demo_role"] = "USER"
        session["demo_user_id"] = self.user.pk
        session.save()
        response = self.client.post(reverse("messaging:detail", args=[self.conversation.pk]), {"body": "A factual follow-up message."})
        self.assertRedirects(response, reverse("messaging:detail", args=[self.conversation.pk]))
        self.assertTrue(Message.objects.filter(conversation=self.conversation, body="A factual follow-up message.").exists())

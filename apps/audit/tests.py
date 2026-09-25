from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory

from .models import AuditEvent
from .services import record_event


class AuditCorrelationTests(TestCase):
    def test_record_event_persists_bounded_request_id(self):
        user = get_user_model().objects.create(username="audit_actor")
        request = RequestFactory().post("/sensitive/")
        request.demo_user_id = user.pk
        request.request_id = "support-ticket-42"

        event = record_event(request, "test.action", metadata={"safe": True})

        self.assertEqual(event.request_id, "support-ticket-42")
        self.assertEqual(event.metadata, {"safe": True})

    def test_missing_request_id_remains_empty(self):
        event = record_event(RequestFactory().get("/health/"), "system.action")

        self.assertEqual(event.request_id, "")

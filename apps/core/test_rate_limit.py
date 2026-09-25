from django.core.cache import cache
from django.test import SimpleTestCase, override_settings
from django.test.client import RequestFactory

from .rate_limit import check_request


class RateLimitMetadataTests(SimpleTestCase):
    @override_settings(RATE_LIMITS={"test": 2}, RATE_LIMIT_WINDOW_SECONDS=30)
    def test_check_returns_remaining_and_retry_metadata(self):
        cache.clear()
        request = RequestFactory().post("/sensitive/")
        request.demo_user_id = 42

        first = check_request(request, "test")
        second = check_request(request, "test")
        third = check_request(request, "test")

        self.assertTrue(first.allowed)
        self.assertEqual(first.remaining, 1)
        self.assertTrue(second.allowed)
        self.assertEqual(second.remaining, 0)
        self.assertFalse(third.allowed)
        self.assertEqual(third.retry_after, 30)

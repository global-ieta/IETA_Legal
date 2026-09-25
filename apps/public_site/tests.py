from django.test import TestCase
from django.urls import reverse

class PublicSeoTests(TestCase):
    def test_sitemap_contains_public_pages_not_private_portals(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("/about/", response.content.decode())
        self.assertNotIn("/portal/", response.content.decode())

    def test_robots_excludes_private_paths(self):
        response = self.client.get(reverse("robots"))
        body = response.content.decode()
        self.assertIn("Disallow: /documents/", body)
        self.assertIn("Sitemap:", body)

    def test_public_page_has_canonical_and_indexing_metadata(self):
        response = self.client.get(reverse("public:page", kwargs={"slug": "about"}))
        self.assertContains(response, 'rel="canonical"')
        self.assertContains(response, 'content="index, follow"')

from django.test import SimpleTestCase, override_settings

from .services import get_private_storage_provider


class PrivateStorageIntegrationTests(SimpleTestCase):
    @override_settings(PRIVATE_STORAGE_BACKEND="local")
    def test_local_provider_is_private_but_not_production_ready(self):
        status = get_private_storage_provider().status()

        self.assertTrue(status.private)
        self.assertTrue(status.operational)
        self.assertFalse(status.production_ready)

    @override_settings(PRIVATE_STORAGE_BACKEND="azure_blob")
    def test_unimplemented_cloud_provider_is_not_operational(self):
        status = get_private_storage_provider().status()

        self.assertEqual(status.backend, "azure_blob")
        self.assertFalse(status.operational)

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.settings.validation import validate_production_environment


class ProductionEnvironmentValidationTests(SimpleTestCase):
    def _valid(self):
        return {
            "DJANGO_SECRET_KEY": "x" * 64,
            "DJANGO_ALLOWED_HOSTS": "legal.example.com,api.example.com",
            "DJANGO_CSRF_TRUSTED_ORIGINS": "https://legal.example.com",
            "DB_ENGINE": "django.db.backends.postgresql",
            "DB_NAME": "ieta",
            "DB_HOST": "postgres.internal",
            "PRIVATE_STORAGE_BACKEND": "azure_blob",
        }

    def test_valid_production_environment_is_accepted(self):
        validate_production_environment(self._valid())

    def test_default_secret_is_rejected(self):
        environment = self._valid()
        environment["DJANGO_SECRET_KEY"] = "replace-in-deployment"
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(environment)

    def test_wildcard_hosts_are_rejected(self):
        environment = self._valid()
        environment["DJANGO_ALLOWED_HOSTS"] = "*"
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(environment)

    def test_sqlite_requires_explicit_override(self):
        environment = self._valid()
        environment["DB_ENGINE"] = "django.db.backends.sqlite3"
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(environment)

    def test_external_database_requires_name_and_host(self):
        environment = self._valid()
        environment.pop("DB_HOST")
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(environment)

    def test_local_private_storage_requires_explicit_override(self):
        environment = self._valid()
        environment["PRIVATE_STORAGE_BACKEND"] = "local"
        with self.assertRaises(ImproperlyConfigured):
            validate_production_environment(environment)

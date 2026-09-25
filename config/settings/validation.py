from django.core.exceptions import ImproperlyConfigured


def validate_production_environment(env):
    """Reject deployment configuration that would silently run unsafely."""
    secret_key = env.get("DJANGO_SECRET_KEY", "")
    if len(secret_key) < 50 or secret_key in {"development-only-change-me", "replace-in-deployment"}:
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be a long, unique production secret.")

    allowed_hosts = [value.strip() for value in env.get("DJANGO_ALLOWED_HOSTS", "").split(",") if value.strip()]
    if not allowed_hosts or "*" in allowed_hosts:
        raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must contain explicit production hosts.")

    csrf_origins = [value.strip() for value in env.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if value.strip()]
    if not csrf_origins or any(not value.startswith("https://") for value in csrf_origins):
        raise ImproperlyConfigured("DJANGO_CSRF_TRUSTED_ORIGINS must contain explicit HTTPS origins.")

    database_engine = env.get("DB_ENGINE", "django.db.backends.sqlite3")
    if database_engine == "django.db.backends.sqlite3" and env.get("ALLOW_PRODUCTION_SQLITE", "false").lower() != "true":
        raise ImproperlyConfigured("Production requires a non-SQLite database unless ALLOW_PRODUCTION_SQLITE=true is explicit.")

    if database_engine != "django.db.backends.sqlite3":
        missing = [name for name in ("DB_NAME", "DB_HOST") if not env.get(name)]
        if missing:
            raise ImproperlyConfigured(f"Missing production database settings: {', '.join(missing)}.")

    if env.get("PRIVATE_STORAGE_BACKEND", "local") == "local" and env.get("ALLOW_LOCAL_PRIVATE_STORAGE", "false").lower() != "true":
        raise ImproperlyConfigured("Production requires a private cloud storage backend unless ALLOW_LOCAL_PRIVATE_STORAGE=true is explicit.")

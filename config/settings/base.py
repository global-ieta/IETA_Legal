"""Shared Django configuration for IETA Legal."""
import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or secrets.token_urlsafe(64)
DEBUG = False
ALLOWED_HOSTS = [host.strip() for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "apps.core", "apps.accounts", "apps.users", "apps.advocates", "apps.intake",
    "apps.matters", "apps.aura", "apps.consultations", "apps.messaging", "apps.calling",
    "apps.privacy", "apps.audit", "apps.notifications", "apps.documents", "apps.admin_portal", "apps.dashboard", "apps.public_site",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", "apps.core.middleware.RequestIDMiddleware", "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware", "apps.core.middleware.DemoRoleMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request", "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages", "apps.core.context_processors.site_context",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/login/"
DEMO_MODE = os.getenv("DEMO_MODE", "True").lower() in {"1", "true", "yes", "on"}
AURA_ENABLED = os.getenv("AURA_ENABLED", "True").lower() in {"1", "true", "yes", "on"}
AURA_API_BASE_URL = os.getenv("AURA_API_BASE_URL", "")
AURA_API_KEY = os.getenv("AURA_API_KEY", "")
AURA_MODEL = os.getenv("AURA_MODEL", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "aura")
AUTH_PROVIDER = os.getenv("AUTH_PROVIDER", "development")
GLOBAL_IETA_API_BASE_URL = os.getenv("GLOBAL_IETA_API_BASE_URL", "")
GLOBAL_IETA_CLIENT_ID = os.getenv("GLOBAL_IETA_CLIENT_ID", "")
GLOBAL_IETA_CLIENT_SECRET = os.getenv("GLOBAL_IETA_CLIENT_SECRET", "")
CALLING_API_BASE_URL = os.getenv("CALLING_API_BASE_URL", "")
CALLING_API_KEY = os.getenv("CALLING_API_KEY", "")
DOCUMENT_SCANNING_API_BASE_URL = os.getenv("DOCUMENT_SCANNING_API_BASE_URL", "")
DOCUMENT_SCANNING_API_KEY = os.getenv("DOCUMENT_SCANNING_API_KEY", "")
PRIVATE_STORAGE_BACKEND = os.getenv("PRIVATE_STORAGE_BACKEND", "local")
NOTIFICATIONS_API_BASE_URL = os.getenv("NOTIFICATIONS_API_BASE_URL", "")
NOTIFICATIONS_API_KEY = os.getenv("NOTIFICATIONS_API_KEY", "")
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMITS = {
    "login": int(os.getenv("RATE_LIMIT_LOGIN", "10")),
    "aura": int(os.getenv("RATE_LIMIT_AURA", "20")),
    "messages": int(os.getenv("RATE_LIMIT_MESSAGES", "30")),
    "documents": int(os.getenv("RATE_LIMIT_DOCUMENTS", "10")),
    "calls": int(os.getenv("RATE_LIMIT_CALLS", "20")),
}
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
MESSAGE_TAGS = {"error": "danger"}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"verbose": {"format": "{levelname} {asctime} {name} {message}", "style": "{"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {"django": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"), "propagate": False}},
}

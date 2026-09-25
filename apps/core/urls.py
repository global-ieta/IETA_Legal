from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse
from django.urls import path
import uuid
from .integration_readiness import get_integration_readiness

def health(request):
    return JsonResponse({"status": "ok", "service": "ieta-legal"})

def readiness(request):
    checks = {}
    try:
        connection.ensure_connection()
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "unavailable"
    cache_key = f"health:{uuid.uuid4().hex}"
    try:
        cache.set(cache_key, "ok", timeout=5)
        checks["cache"] = "ok" if cache.get(cache_key) == "ok" else "unavailable"
    except Exception:
        checks["cache"] = "unavailable"
    ready = all(value == "ok" for value in checks.values())
    return JsonResponse({"status": "ready" if ready else "not_ready", "service": "ieta-legal", "checks": checks}, status=200 if ready else 503)

def integrations(request):
    return JsonResponse({
        "status": "configuration-report",
        "service": "ieta-legal",
        "network_calls": False,
        "integrations": get_integration_readiness(),
    })

urlpatterns = [
    path("", health, name="health"),
    path("live/", health, name="health_live"),
    path("ready/", readiness, name="health_ready"),
    path("integrations/", integrations, name="health_integrations"),
]

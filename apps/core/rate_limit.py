import hashlib
from dataclasses import dataclass
from django.core.cache import cache
from django.conf import settings

def _key(request, bucket):
    identity = str(getattr(request, "demo_user_id", None) or request.META.get("REMOTE_ADDR", "anonymous"))
    digest = hashlib.sha256(identity.encode()).hexdigest()[:24]
    return f"ieta-rate:{bucket}:{digest}"

@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    retry_after: int


def check_request(request, bucket, limit=None, window=None):
    """Check a cache-backed limit and return safe response metadata."""
    limit = limit if limit is not None else settings.RATE_LIMITS.get(bucket, 30)
    window = window if window is not None else settings.RATE_LIMIT_WINDOW_SECONDS
    key = _key(request, bucket)
    if cache.add(key, 1, timeout=window):
        count = 1
    else:
        try:
            count = cache.incr(key)
        except ValueError:
            count = 1
            cache.set(key, count, timeout=window)
    return RateLimitResult(allowed=count <= limit, limit=limit, remaining=max(limit - count, 0), retry_after=window)


def allow_request(request, bucket, limit=None, window=None):
    """Compatibility helper for callers that only need the boolean result."""
    return check_request(request, bucket, limit=limit, window=window).allowed


def apply_rate_limit_headers(response, result):
    response["X-RateLimit-Limit"] = str(result.limit)
    response["X-RateLimit-Remaining"] = str(result.remaining)
    if not result.allowed:
        response["Retry-After"] = str(result.retry_after)
    return response

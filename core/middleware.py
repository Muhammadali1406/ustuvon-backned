from __future__ import annotations

import logging
import time

from django.core.cache import caches
from django.http import JsonResponse


logger = logging.getLogger("django.request")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.perf_counter()
        response = self.get_response(request)
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)

        logger.info(
            "HTTP %s %s -> %s in %.2fms remote=%s user=%s",
            request.method,
            request.path,
            getattr(response, "status_code", "unknown"),
            duration_ms,
            request.META.get("REMOTE_ADDR", "unknown"),
            getattr(request.user, "pk", None),
        )
        return response


class RateLimitMiddleware:
    """A lightweight request limiter for API routes using Django cache backend."""

    RATE_LIMIT = 60
    WINDOW_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response
        self.cache = caches["default"]

    def _get_client_key(self, request) -> str:
        return f"ratelimit:{request.META.get('REMOTE_ADDR', 'unknown')}:{request.path}"

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        key = self._get_client_key(request)
        current_count = self.cache.get(key, 0)

        if current_count >= self.RATE_LIMIT:
            return JsonResponse(
                {"detail": "Siz juda ko'p so'rov yubordingiz. Bir ozdan keyin qayta urinib ko'ring."},
                status=429,
            )

        self.cache.set(key, current_count + 1, timeout=self.WINDOW_SECONDS)
        return self.get_response(request)

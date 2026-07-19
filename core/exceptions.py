from __future__ import annotations
import logging
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_default_exception_handler


logger = logging.getLogger(__name__)

class ServiceError(Exception):
    code = "service_error"
    message = "Kutilmagan xatolik yuz berdi."
    status_code = 400

    def __init__(self, message: str | None = None, details: dict | None = None):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)



class NotFoundServiceError(ServiceError):
    code = "not_found"
    message = "Obyekt topilmadi."
    status_code = 404



class PermissionDeniedServiceError(ServiceError):
    code = "permission_denied"
    message = "Bu amalni bajarishga ruxsatingiz yo'q."
    status_code = 403



class ConflictServiceError(ServiceError):

    code = "conflict"
    message = "Bu amal hozircha bajarilishi mumkin emas."
    status_code = 409

def _error_response(code: str, message: str, status_code: int, details: dict | None = None) -> Response:
    return Response(
        {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
            },
        },
        status=status_code,
    )


def custom_exception_handler(exc, context):

    if isinstance(exc, ServiceError):
        return _error_response(exc.code, exc.message, exc.status_code, exc.details)

    if isinstance(exc, Http404):
        exc = drf_exceptions.NotFound()

    elif isinstance(exc, DjangoPermissionDenied):
        exc = drf_exceptions.PermissionDenied()

    response = drf_default_exception_handler(exc, context)

    if response is None:
        logger.exception("Unhandled exception in %s", context.get("view"))
        return _error_response("internal_error", "Serverda xatolik yuz berdi.", 500)

    code = getattr(exc, "default_code", exc.__class__.__name__.lower())
    if isinstance(response.data, dict) and "detail" in response.data:
        message = str(response.data["detail"])
        details = {}
    else:
        message = "So'rovda xatolik bor."
        details = response.data if isinstance(response.data, dict) else {"errors": response.data}


    return _error_response(code, message, response.status_code, details)
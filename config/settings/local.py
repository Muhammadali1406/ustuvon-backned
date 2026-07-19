"""
Local development settings.
Run with:  DJANGO_SETTINGS_MODULE=config.settings.local
"""
from .base import *  # noqa: F401,F403




DEBUG = True
ALLOWED_HOSTS = ["*"]




# --------------------------------------------------------------------------
# Debug toolbar
# --------------------------------------------------------------------------
INSTALLED_APPS += [
    "debug_toolbar",
]
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE
INTERNAL_IPS = ["127.0.0.1"]




# --------------------------------------------------------------------------
# Email — print to console instead of sending real messages
# --------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"




# --------------------------------------------------------------------------
# CORS — wide open for local frontend dev
# --------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True




# --------------------------------------------------------------------------
# DRF — enable the browsable API for manual testing
# --------------------------------------------------------------------------
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (
    "rest_framework.renderers.BrowsableAPIRenderer",
)




# --------------------------------------------------------------------------
# Celery — run tasks synchronously so you don't need a worker running
# --------------------------------------------------------------------------
CELERY_TASK_ALWAYS_EAGER = env.bool("CELERY_TASK_ALWAYS_EAGER", default=True)
CELERY_TASK_EAGER_PROPAGATES = True
LOGGING["root"]["level"] = "DEBUG"
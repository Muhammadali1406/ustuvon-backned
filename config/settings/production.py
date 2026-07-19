"""
Production settings — strict security, no debug, everything from env vars.
Run with:  DJANGO_SETTINGS_MODULE=config.settings.production
"""
from .base import *  # noqa: F401,F403




DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_ALL_ORIGINS = False





# --------------------------------------------------------------------------
# Email & Ohirgacha bitkazish kerek
# --------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)





# --------------------------------------------------------------------------
# Security hardening
# --------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")






# --------------------------------------------------------------------------
# Static files — served by WhiteNoise behind Nginx
# --------------------------------------------------------------------------
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")






# --------------------------------------------------------------------------
# Error monitoring
# --------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN", default="")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        environment="production",
        traces_sample_rate=0.1,
        send_default_pii=False,
    )




# --------------------------------------------------------------------------
# Logging — quieter, no DEBUG noise in prod
# --------------------------------------------------------------------------
LOGGING["handlers"]["console"]["formatter"] = "verbose"
LOGGING["root"]["level"] = "WARNING"
LOGGING["loggers"]["django"]["level"] = "WARNING"
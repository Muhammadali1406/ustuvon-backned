from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)




API_PREFIX = "api/v1/"






urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(f"{API_PREFIX}auth/", include("apps.users.urls")),
    path(f"{API_PREFIX}subjects/", include("apps.subjects.urls")),
    path(f"{API_PREFIX}exams/", include("apps.exams.urls")),
    path(f"{API_PREFIX}results/", include("apps.results.urls")),
    path(f"{API_PREFIX}statistics/", include("apps.statistics.urls")),
    path(f"{API_PREFIX}certificates/", include("apps.certificates.urls")),
    path(f"{API_PREFIX}notifications/", include("apps.notifications.urls")),
    path(f"{API_PREFIX}payments/", include("apps.payments.urls")),  
    path(f"{API_PREFIX}ai-parser/", include("apps.ai_parser.urls")),
    path(f"{API_PREFIX}admin-panel/", include("apps.admin_panel.urls")),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
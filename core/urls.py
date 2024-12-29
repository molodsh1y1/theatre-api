from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-theatre/", include("theatre.urls", namespace="theatre")),
    path("api-accounts/", include("accounts.urls", namespace="accounts")),
    path(
        "api/doc/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    path(
        "api/doc/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc"
    ),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

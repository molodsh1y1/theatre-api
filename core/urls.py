from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api-theatre/", include("theatre.urls", namespace="theatre")),
    path("api-accounts/", include("accounts.urls", namespace="accounts"))
]

from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from . import settings

urlpatterns = [
    path("", include("chat.urls")),
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL)
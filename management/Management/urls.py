from django.contrib import admin
from django.urls import path, include

from Login.urls import login_urls

urlpatterns = [
    path("login/", include(login_urls)),
    path("admin/", admin.site.urls),
]

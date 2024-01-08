from django.contrib import admin
from django.urls import path, include

from Login.urls import login_urls
from Character.urls import character_urls
from Map.urls import map_urls

urlpatterns = [
    path("login/", include(login_urls)),
    path("character/", include(character_urls)),
    path("map/", include(map_urls)),
    path("admin/", admin.site.urls),
]

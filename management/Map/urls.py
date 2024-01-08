from django.urls import include, path
from rest_framework import routers

from Map import views

map_router = routers.DefaultRouter()
map_router.register("map", views.MapViewSet)

map_urls = map_router.urls

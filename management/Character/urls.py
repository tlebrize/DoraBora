from rest_framework import routers

from Character import views

character_router = routers.DefaultRouter()
character_router.register("character", views.CharacterViewSet)

character_urls = character_router.urls

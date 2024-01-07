from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as token_views

from Login import views

login_router = routers.DefaultRouter()
login_router.register("account", views.AccountViewSet)
login_router.register("server", views.ServerViewSet)

login_urls = login_router.urls
login_urls += [path("token/", token_views.obtain_auth_token)]

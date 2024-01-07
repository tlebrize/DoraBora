from django.contrib import admin

from Login.models import Account, Server
from rest_framework.authtoken.models import Token


admin.site.register(Server)
admin.site.register(Account)

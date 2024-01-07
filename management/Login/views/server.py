from rest_framework import viewsets, permissions, mixins

from Login.models import Server
from Login.serializers import ServerSerializer


class ChangeServerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "GET":
            return request.user.has_perm("Login.change_server")

        else:
            return True


class ServerViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = [ChangeServerPermission]

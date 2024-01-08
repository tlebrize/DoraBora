from rest_framework import viewsets, permissions

from Map.models import Map
from Map.serializers import MapSerializer


class MapViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MapSerializer
    queryset = Map.objects.all()
    permission_classes = [permissions.AllowAny]

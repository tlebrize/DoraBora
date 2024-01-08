from rest_framework import viewsets, mixins, permissions
from Character.models import Character
from Character.serializers import CharacterSerializer


class CharacterViewSet(
    viewsets.ReadOnlyModelViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return self.queryset.filter(
            account_id=self.request.query_params["account_id"],
            server_id=self.request.query_params["server_id"],
        )

from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from Login.models import Account
from Login.serializers import AccountSerializer


class AccountViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # def get_queryset(self):
    #     return self.queryset.filter(dj_user=self.request.user)

    permission_classes = [permissions.AllowAny]  # needed for get_account_by_id

    @action(detail=False, methods=["get"])
    def me(self, request):
        return Response(
            self.serializer_class(
                instance=self.queryset.filter(dj_user=self.request.user).get(),
            ).data,
        )

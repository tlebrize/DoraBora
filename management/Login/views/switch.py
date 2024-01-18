from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from Login.models import Account


@api_view(["POST"])
def switch_view(request):
    switch_token = request.data.get("switch_token")
    key = Token.objects.get(user__account__switch_token=switch_token).key
    Account.objects.filter(switch_token=switch_token).update(switch_token=None)
    return Response({"token": key})

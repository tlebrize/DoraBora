from rest_framework import serializers
from django.utils import timezone

from Login.models import Account


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="dj_user.username")
    subscribed_seconds = serializers.SerializerMethodField()
    is_game_master = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "nickname",
            "state",
            "subscribed_seconds",
            "is_game_master",
            "security_question",
            "community",
        ]
        read_only_fields = [
            "id",
            "username",
            "nickname",
            "subscribed_seconds",
            "is_game_master",
            "security_question",
            "community",
        ]

    def get_subscribed_seconds(self, obj):
        if obj.subscribed_until > timezone.now():
            return (obj.subscribed_until - timezone.now()).seconds
        else:
            return 0

    def get_is_game_master(self, obj):
        return obj.dj_user.is_staff

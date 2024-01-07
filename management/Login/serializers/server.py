from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from Login.models import Server


class ServerSerializer(serializers.ModelSerializer):
    character_count = serializers.SerializerMethodField(source="get_character_count")

    class Meta:
        model = Server
        fields = [
            "id",
            "name",
            "host",
            "port",
            "state",
            "subscriber_only",
            "character_count",
        ]

    def get_character_count(self, obj):
        try:
            return self.context.get("request").user.account.characters.filter(server=obj).count()
        except ObjectDoesNotExist:
            return 0

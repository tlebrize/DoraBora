from rest_framework import serializers

from Character.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    map_dofus_id = serializers.IntegerField(source="map.dofus_id")

    class Meta:
        model = Character
        fields = [
            "id",
            "account_id",
            "map_id",
            "map_dofus_id",
            "server_id",
            "_class",
            "colors",
            "energy",
            "gender",
            "kamas",
            "level",
            "name",
            "spell_points",
            "stat_points",
            "experience",
        ]
        read_only_fields = fields

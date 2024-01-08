from rest_framework import serializers

from Character.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    map_dofus_id = serializers.IntegerField(source="map.dofus_id", read_only=True)

    class Meta:
        model = Character
        fields = [
            "id",
            "account",
            "map",
            "map_dofus_id",
            "server",
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
        read_only_fields = ["id", "map_dofus_id"]

    def create(self, validated_data):
        if not validated_data.get("map"):
            validated_data["map_id"] = 5749
        return super().create(validated_data)

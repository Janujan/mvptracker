from rest_framework import serializers
from .models import Player, Game


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("player_name", "player_team")

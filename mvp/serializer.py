from rest_framework import serializers
from .models import Player, Game


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("player_name","player_team","ppg", "apg", "rpg", "tpg", "ascore")

class GameSerializer(serializers.ModelSerializer):
    #player = PlayerSerializer()
    class Meta:
        model = Game
        fields = ("start_time", "points", "assists", "rebounds", "turnovers","gmscre")
class PlayerDetailSerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True)

    class Meta:
        model = Player
        fields = ("player_name","player_team","ppg", "apg", "rpg", "tpg", "ascore", "games")

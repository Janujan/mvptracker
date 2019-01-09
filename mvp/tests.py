from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Player, Game
from .serializer import PlayerSerializer
import json
# tests for views
class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_player(name="", team=""):
        if name != "" and team != "":
            Player.objects.create(player_name=name, player_team=team)

    def setUp(self):
        # add test data
        self.create_player("Micheal Jordan", "Chicago Bulls")
        self.create_player("Kobe Bryant", "Losangelos Lakers")
        self.create_player("Steve Nash", "Phoenix Suns")
        self.create_player("Ron Artest", "Houston Rockets")

class GetAllPlayersTest(BaseViewTest):

    def test_get_all_players(self):
        """
        Check that all players returned by API endpoint match the players in
        database
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("mvp:playersList")
        )
        # fetch the data from db
        expected = Player.objects.all()
        serialized = PlayerSerializer(expected, many=True)
        self.assertEqual(response.json(), serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

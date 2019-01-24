from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import OutputType
from bball_wrapper import Ball_Player
import os
import django

# # replace project_name with your own project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mvptracker.settings")
django.setup()
#from datadump import Dd
from mvp.models import Player, Game


season_totals = client.players_season_totals(season_end_year=2019)

#print(season_totals[0:10])

print(len(season_totals))


current_players = Player.objects.all()

names = {}
for player in current_players:
    names[player.player_name] = player

print(Player.objects.order_by('ascore')[0:5])

for player in season_totals:
    if player['name'] in names:
        print('found this name again: ' + player['name'])

    else:
        p = Ball_Player(player['name'])
        p.populateLive(player)
        pp = Player(player_name = player['name'])
        pp.copy(p)
        pp.save()
        del pp
        del p

"""""
output:
- add all 500 other players, excluding the 10 players that are already stored!

Thoughts:
- load all current player names into a dictionary
- compare each new player to one in dictionary
- if they match, dont Add
- else, create player object, populate player and add to db!
"""""

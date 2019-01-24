# from bball_wrapper import Ball_Player
# from bball_wrapper import Game as game
# from datetime import datetime, timezone, tzinfo
# from datadump import Dd
#
# from django.contrib.gis.db import models as gis_models
#
# #this is to update player averages and add new games
#
# d = Dd()
# d.updateGames()

import os
import django

# replace project_name with your own project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mvptracker.settings")
django.setup()
from datadump import Dd

d = Dd()
#d.updateStats()
d.updatePlayer()

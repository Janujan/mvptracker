from bball_wrapper import Ball_Player
from bball_wrapper import Game as game

from mvp.models import Player, Game
from datetime import datetime, timezone, tzinfo

class Dd:
    names = [
    'James Harden',
    'Stephen Curry',
    'LeBron James',
    'Kevin Durant',
    'Russell Westbrook',
    'Joel Embiid',
    'Kawhi Leonard',
    'Anthony Davis',
    'Giannis Antetokounmpo',
    'Damian Lillard'
    ]

    def delete_old(self):
        p = Player.objects.all()
        g = Game.objects.all()

        p.delete()
        g.delete()
        del p,g

    def dumpdata(self):
        print('dumping data')

        #create player, find all game days, get all game scores, add to database
        for name in self.names:
            player = Ball_Player(name)
            player.populate()
            pp = Player(player_name = player.name)
            pp.copy(player)
            pp.save()
            player.print()

            game_days = player.get_all_games()
            #print(game_days)
            for games in game_days:
                g = game(games, player.name)
                flag = g.get_box_score()
                if flag:
                    g.update()
                    gg = Game(start_time = g.date, player = pp)
                    gg.copy(g)
                    gg.save()
                    del gg
                else:
                    print('Player did not play')

                del g

            del pp
            del player

    def updateScore(self):
        print('updating a score')

        players = Player.objects.all()

        for player in players:
            player.ascore = player.ppg + player.apg + player.rpg
            player.save()

    def player_avg_Update(self):
        print('Setting new averages games')

        players = Player.objects.all()

        for player in players:
            play = Ball_Player(player.player_name)
            play.populate()
            player.copy(play)
            player.save()
            del play

    def updatePlayer(self):
        for name in self.names:
            player = Ball_Player(name)
            player.populate()
            pp = Player.objects.get(player_name = name)
            pp.copy(player)
            pp.save()
            player.print()
            del pp
            del player


    def updateStats(self):

        player_list= Player.objects.all()
        for player in player_list:

            #get new player stats
            player = Ball_Player(player.player_name)
            player.populate()

            #get player object to get appriopriate id for each game added
            pp = Player.objects.get(player_name= player.name)
            sched = player.get_all_games()

            #retrieve the last game stored
            games = pp.game_set.order_by('start_time')
            size = len(games)
            last_game_stored = games[size-1]

            #go through last 5 games and update new games
            for x in range(1,6):
                game_day = sched[-x]
                if (game_day - last_game_stored.start_time).days>0:
                    g = game(game_day, player.name)
                    flag = g.get_box_score()
                    if flag:
                        g.update()
                        g.print()
                        gg = Game(start_time = g.date, player = pp)
                        gg.copy(g)
                        print(gg)
                        gg.save()
                        del gg
                    else:
                        print('Player did not play')
                    del g
            pp.save()
            del pp
            del player

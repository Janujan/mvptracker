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

            game_days = player.get_last_five_games()
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

    def updateGames(self):

        players = Player.objects.all()
        today = datetime.now(timezone.utc)

        # for player in players:
        #     games = player.game_set.order_by('-start_time')
        #     latest_game = games[0]
        #
        #     play = Ball_Player(player.player_name)
        #     play.populate()
        #
        #     schedule = play.get_last_five_games(latest_game.start_time)
        #
        #     for day in schedule:
        #         g = game(day, player.player_name)
        #         print(day)
        #         flag = g.get_box_score()
        #         if flag:
        #             g.update()
        #             gg = Game(start_time = g.date, player = player)
        #             gg.copy(g)
        #             print(gg.player)
        #             gg.save()
        #             del gg
        #         else:
        #             print('Player did not play')
        #         del g

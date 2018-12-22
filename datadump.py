from bball_wrapper import Ball_Player
from bball_wrapper import Game as game

from mvp.models import Player, Game

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

            game_days = player.get_last_five_games()
            for games in game_days:
                print(games)
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

from bball_wrapper import Ball_Player
from bball_wrapper import Game as game
from basketball_reference_web_scraper import client


from mvp.models import Player, Game
from datetime import datetime, timezone, tzinfo, timedelta

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
            player.ascore = player.ppg + player.apg + (0.7)*player.rpg
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

        season_totals = client.players_season_totals(season_end_year=2019)

        for player in season_totals:
            player_obj = Ball_Player(player['name'])
            player_obj.populateLive(player)
            pp = Player.objects.filter(player_name = player_obj.name)
            if len(pp) > 1:
                ppp = Player.objects.filter(player_name = player_obj.name)[1]
                ppp.delete()
            pp = Player.objects.filter(player_name = player_obj.name)[0]
            print(pp)
            pp.copy(player_obj)
            pp.save()
            del pp
            del player_obj

    def updateStats(self):

        player_list= Player.objects.order_by('ascore').reverse()[0:10]

        for player in player_list:
            #get new player stats
            player_obj = Ball_Player(player.player_name)
            player_obj.copy(player)
            sched = player_obj.get_all_games()
            print(sched)
            #retrieve the last game stored
            games = player.games.order_by('start_time')
            size = len(games)
            if size == 0:
                last_game_stored = sched[-10]
                print(last_game_stored)
            else:
                last_game_stored = games[size-1].start_time

            #go through last 5 games and update new games
            for x in range(1,6):
                game_day = sched[-x]
                if (game_day - last_game_stored).days>0:
                    g = game(game_day, player_obj.name)
                    flag = g.get_box_score()
                    if flag:
                        g.update()
                        g.print()
                        gg = Game(start_time = g.date, player = player)
                        gg.copy(g)
                        print(gg)
                        gg.save()
                        del gg
                    else:
                        print('Player did not play')
                    del g
                else:
                    print('skipped game')

            del player

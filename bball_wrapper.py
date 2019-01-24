from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import OutputType
from datetime import datetime, timezone, tzinfo
from pytz import timezone as tz
#import matplotlib.pyplot as plt

threes = 'made_three_point_field_goals'
fgs = 'made_field_goals'
fts = 'made_free_throws'
gp = 'games_played'
def_reb = 'defensive_rebounds'
off_reb = 'offensive_rebounds'
ast = 'assists'
tov = 'turnovers'
team = 'team'

class Ball_Player:

    season_totals = []
    last_games = []
    sched = []
    def __init__(self, name):
        self.name = name
        self.team = None
        self.ppg = 0
        self.reb = 0
        self.ast = 0
        self.tov = 0
        self.gp = 0

    #get a player model and copy teeam info
    def copy(self, player):
        self.team = player.player_team.value

    #return points per game
    def points_per_game( self, player ):

        point_threes = player[threes]*3
        point_twos = (player[fgs] - player[threes])*2
        point_ones = player[fts]
        total_points = point_threes + point_twos + point_ones
        ppg = total_points/self.gp

        return ppg

    #return rebounds per game
    def rebs_per_game( self, player):
        def_rebounds = player[def_reb]
        off_rebounds = player[off_reb]
        return (def_rebounds + off_rebounds)/self.gp


    #return the player stats given name and full season stats (filtering)
    def get_player( self, player_name, season_totals ):
        player = list(filter(lambda person: person['name'] == player_name, season_totals))
        return player

    #return the games that specified player has played in (avoid injuries)
    def games_played(self, player):
        team = player['team']
        total_games = player[gp]
        return total_games

    #return assists per game
    def asts_per_game(self, player):
        assists = player[ast]
        return assists/self.gp

    #return team that player is on
    def get_team(self, player):
        player_team = player[team]
        return player_team

    #return turnovers per game
    def tov_per_game(self, player):
        turnovers = player[tov]/self.gp
        return turnovers

    #update all stats for player object
    def populate(self, pop):
        self.get_season_totals()
        self.gp = self.games_played(pop)
        self.ppg = self.points_per_game(pop)
        self.reb = self.rebs_per_game(pop)
        self.ast = self.asts_per_game(pop)
        self.tov = self.tov_per_game(pop)
        self.team = self.get_team(pop)

    def populateLive(self, pop):
        self.gp = self.games_played(pop)
        self.ppg = self.points_per_game(pop)
        self.reb = self.rebs_per_game(pop)
        self.ast = self.asts_per_game(pop)
        self.tov = self.tov_per_game(pop)
        self.team = self.get_team(pop)

    def print(self):
        print(self.name)
        print(self.team)
        print('Per Game Points')
        print(self.ppg)
        print('Per Game Rebounds')
        print(self.reb)
        print('Per Game Assists')
        print(self.ast)

    def __str___(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

    #return all player season totals, make this year adjustable
    def get_season_totals(self):
        self.season_totals = client.players_season_totals(season_end_year=2019)

    #return all games played by team
    def get_all_games(self):
        schedule = client.season_schedule(season_end_year=2019)
        games = []
        today = datetime.now(timezone.utc)

        #one day offset
        yesterday = today.day - 1
        today = today.replace(day=yesterday)

        for game in schedule:
            game_day = game['start_time']
            if((today - game_day).days >= 0 ):
                if( game['home_team'].value == self.team):
                    games.append(game['start_time'])
                elif( game['away_team'].value == self.team):
                    games.append(game['start_time'])
        return games


class Game:
    box_score = []

    def __init__(self, date, name):
        self.name = name
        self.date = date
        self.pts = 0
        self.asts = 0
        self.rebs = 0
        self.tov = 0
        self.gmscre = 0

    # populate all variables once box_score is retrieved
    def update(self):
        self.pts = self.update_points(self.box_score)
        self.rebs = self.update_rebounds(self.box_score)
        self.asts = self.update_assists(self.box_score)
        self.tov = self.update_tov(self.box_score)
        self.gmscre = self.update_gmsc(self.box_score)

    def update_points(self, player):
        point_threes = player[0][threes]*3
        point_twos = (player[0][fgs] - player[0][threes])*2
        point_ones = player[0][fts]
        total_points = point_ones + point_threes +point_twos
        return total_points

    def update_rebounds(self, player):
        rebs = player[0][def_reb] + player[0][off_reb]
        return rebs

    def update_assists(self, player):
        asts = player[0][ast]
        return asts

    def update_tov(self, player):
        tovs = player[0][tov]
        return tovs

    def update_gmsc(self, player):
        gmscr = player[0]['game_score']
        return gmscr

    #retrieve the box_score for the game played by this player
    def get_box_score(self):
        est = tz('US/Eastern')
        self.date = self.date.astimezone(est)
        player_scores = client.player_box_scores(self.date.day, self.date.month, self.date.year)
        self.box_score = list(filter(lambda person: person['name'] == self.name, player_scores))
        #make sure box_score is not empty
        if self.box_score:
            return True
        else:
            return False

    def __repr__(self):
        return str(self.date)

    def __str__(self):
        return str(self.date)

    def print(self):
        print('Points')
        print(self.pts)
        print('Assists')
        print(self.asts)
        print('Rebs')
        print(self.rebs)
        print('Turnovers')
        print(self.tov)
        print('Game Score')
        print(self.gmscre)

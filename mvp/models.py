from django.db import models
from django.utils import timezone

# Create your models here.

class Player(models.Model):
    player_name = models.CharField(max_length=200)
    player_team = models.CharField(max_length=200)
    ppg = models.IntegerField()
    apg = models.IntegerField()
    rpg = models.IntegerField()
    tpg = models.IntegerField()
    ascore = models.IntegerField( default = 0)
    def __str__(self):
        return self.player_name

    #take player object from bball_wrapper and convert to datebase entry
    def copy(self, player):
        self.player_name = player.name
        self.team = player.team
        self.ppg = player.ppg
        self.apg = player.ast
        self.rpg = player.reb
        self.tpg = player.tov
        self.ascore = self.ppg + self.apg + self.rpg - self.tpg

class Game(models.Model):
    player = models.ForeignKey(Player,on_delete=models.CASCADE)
    start_time = models.DateTimeField('game day')
    points = models.IntegerField()
    assists = models.IntegerField()
    rebounds = models.IntegerField()
    turnovers = models.IntegerField()
    gmscre = models.IntegerField()

    #take game object from bball_wrapper and convert to datebase entry
    def copy(self, game_class):
        self.points = game_class.pts
        self.start_time = game_class.date
        self.assists = game_class.asts
        self.rebounds = game_class.rebs
        self.turnovers = game_class.tov
        self.gmscre = game_class.gmscre


    def __str__(self):
        return str(self.start_time)

class Blog(models.Model):
    author = models.CharField(max_length = 200)
    pub_date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    date_created = models.DateTimeField(default = timezone.now())

    def publish(self):
        self.pub_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

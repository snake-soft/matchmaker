from django.db import models
from player.models import Player


class Team(models.Model):
    teamname = models.CharField(max_length=50, verbose_name="Teamname")
    players = models.ManyToManyField(Player)

    def get_team_score(self):
        ''' calculate based on matches '''
        return 1

    def __str__(self):
        return str("%s" % (self.teamname))

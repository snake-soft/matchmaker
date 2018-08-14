from django.db import models
from player.models import Player


class Team(models.Model):
    teamname = models.CharField(max_length=50, verbose_name="Teamname")
    players = models.ManyToManyField(Player)

    tscore = models.PositiveIntegerField(
        verbose_name="Player Score",
        default=1000
        )

    def get_team_score(self):
        ''' calculate based on matches '''
        return self.tscore

    def __str__(self):
        return str(
            "%s (TeamScore: %s; Members: %s)" % (
                self.teamname,
                self.get_team_score(),
                ", ".join([x.nick for x in self.players.all()])
                )
            )

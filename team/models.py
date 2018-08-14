from django.db import models
from player.models import Player
from django.core.validators import MinValueValidator


class Team(models.Model):
    teamname = models.CharField(max_length=50, verbose_name="Teamname")
    players = models.ManyToManyField(Player)

    tscore = models.FloatField(
        verbose_name="Team Score",
        default=0,
        validators=[MinValueValidator(0.0)],
        )

    def get_team_score(self):
        ''' calculate based on matches '''
        return self.tscore

    def get_team_rating(self):
        """ Calculates the team strength out of the Player Elo """
        return sum([x.get_player_rating() for x in self.players.all()])

    def __str__(self):
        return str(
            "%s (TeamScore: %s; TeamRating: %s Members: %s)" % (
                self.teamname,
                self.get_team_score(),
                self.get_team_rating(),
                ", ".join([x.nick for x in self.players.all()])
                )
            )

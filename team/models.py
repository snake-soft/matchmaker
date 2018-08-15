from django.db import models
from django.core.validators import MinValueValidator

from player.models import Player


class Team(models.Model):
    """ Teams are Season-based -> every season there are new values """
    teamname = models.CharField(
        max_length=50, verbose_name="Teamname",
        blank=True
        )
    players = models.ManyToManyField(Player)

    tscore = models.PositiveSmallIntegerField(
        verbose_name="Team Score",
        default=0,
        validators=[MinValueValidator(0.0)],
        )

    def new_result(self, own_goals, foreign_goals):
        if own_goals == foreign_goals:
            self.tscore += 1
        elif own_goals > foreign_goals:
            self.tscore += 2
        self.save()

    @property
    def team_score(self):
        ''' calculate based on matches '''
        return self.tscore

    @property
    def team_rating(self):
        """ Calculates the team strength out of the Player Elo """
        return sum([x.player_rating for x in self.players.all()])

    def get_team_name_or_members(self):
        if self.teamname:
            return self.teamname
        else:
            return ', '.join([x.nick for x in self.players.all()])

    def __str__(self):
        return str(
            "%s (TeamScore: %s; TeamRating: %s Members: %s)" % (
                self.get_team_name_or_members(),
                int(self.team_score + 0.5),
                int(self.team_rating + 0.5),
                ", ".join([x.nick for x in self.players.all()])
                )
            )

#===============================================================================
# class TeamStats:
#     from match.models import Match
#     TeamStats.Match.objects.filter(firstteam=1)
#===============================================================================

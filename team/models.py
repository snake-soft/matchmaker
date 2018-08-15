from django.db import models
from player.models import Player
from django.core.validators import MinValueValidator


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

    def get_games_played(self):
        return 1

    def get_team_score(self):
        ''' calculate based on matches '''
        return self.tscore

    def get_team_rating(self):
        """ Calculates the team strength out of the Player Elo """
        return sum([x.get_player_rating() for x in self.players.all()])

    def get_team_name_or_members(self):
        if self.teamname:
            return self.teamname
        else:
            return ', '.join([x.nick for x in self.players.all()])

    def __str__(self):
        self.get_team_name_or_members()
        return str(
            "%s (TeamScore: %s; TeamRating: %s Members: %s)" % (
                self.get_team_name_or_members(),
                int(self.get_team_score() + 0.5),
                int(self.get_team_rating() + 0.5),
                ", ".join([x.nick for x in self.players.all()])
                )
            )

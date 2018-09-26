""" model for player objects """
from django.db import models

from django.contrib.auth.models import AbstractUser

from core.models import PlayerTeamBase
from team.models import Team
from elo.models import Elo


class Player(PlayerTeamBase, AbstractUser):
    email = models.EmailField(null=True, blank=True)

    elos = models.ManyToManyField('match.Match', through='elo.Elo', through_fields=('player', 'match'))

    communities = models.ManyToManyField(
        'community.Community', blank=True,
        through='community.CommunityMembership')

    active_community = models.ForeignKey(
        'community.Community', blank=True, related_name='active_community',
        null=True, on_delete=models.SET_NULL)

    @property
    def strength(self):
        return int(str(self.elo)) if self.elo else 1000

    @property
    def elo(self):
        return self.elo_set.latest() if self.elo_set.all() else False

    #===========================================================================
    # @strength.setter
    # def strength(self, match):
    #     pass
    #===========================================================================

    @property
    def teams(self):
        return [None]  # team_set

    @property
    def score(self):
        return sum([team.score for team in self.teams])

    @property
    def get_players(self):
        return [self]
    players = get_players

    def new_result(self, match):
        return Elo.new_result(player=self, match=match)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s (%s)' % (
            self.name if self.name else self.username, str(self.elo))


#=========================================================================
# class Player(models.Model):
#     """ Player stats are long-term statistics that are not deleted """
#     owner = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#     )
#     nick = models.CharField(
#         max_length=50, verbose_name="Nickname"
#     )
#
#     rating = models.FloatField(
#         verbose_name="Player Rating",
#         default=1000,
#         validators=[MinValueValidator(0.0)],
#     )
#
#     def new_result(self, goal_diff, enemy):
#         """ calculate new elo """
#         elo = Elo(self.rating)
#         self.rating = elo.new_result(enemy.team_rating, goal_diff)
#         self.save()
#
#     @property
#     def rating_as_int(self):
#         """ return rating as int """
#         return self.player_rating(as_int=True)
#
#     @property
#     def score(self):
#         return sum([team.team_score for team in self.teams()])
#
#     def player_rating(self, as_int=False):
#         """ return player rating """
#         return int(self.rating + 0.5) if as_int else self.rating
#
#     def teams(self):
#         """ return teams of this player """
#         ret = Team.objects.filter(players=self.pk)
#         return ret
#
#     def get_win_draw_lose(self):
#         """ returns tuple of three lists ([win], [draw], [lose]) """
#         win, draw, lose = [], [], []
#         for team in self.teams():
#             team_results = team.get_win_draw_lose
#             win += team_results[0]
#             draw += team_results[1]
#             lose += team_results[2]
#         return win, draw, lose
#
#     @property
#     def matches_chronologic(self):
#         lst_of_lsts = [team.matches_chronologic for team in self.teams()]
#         return sorted([y for x in lst_of_lsts for y in x])
#
#     def get_close_win_lose(self):
#         """ returns tuple of two lists ([close win], [close lose]) """
#         win, lose = [], []
#         for team in self.teams():
#             team_results = team.close_win_lose
#             win += team_results[0]
#             lose += team_results[1]
#         return win, lose
#
#     def save(self, *args, **kwargs):  # pylint: disable=W0221
#         new = False if self.pk else True
#         if new:
#             if Player.objects.filter(nick__iexact=self.nick, owner=self.owner):
#                 raise ValueError("Player %s exists already." % (self.nick))
#
#             if Team.objects.filter(
#                     teamname__iexact=self.nick, owner=self.owner):
#                 raise ValueError("Team %s exists already." % (self.nick))
#
#         super().save(*args, **kwargs)
#         if new:
#             team = Team.objects.create(
#                 teamname=self.nick,
#                 owner=self.owner,
#             )
#             team.players.add(self)
#
#     def __eq__(self, other):
#         return self.pk == other.pk
#
#     def __lt__(self, other):
#         if not self.matches_chronologic:
#             return False
#         if self.player_rating() != other.player_rating():
#             return self.player_rating() > other.player_rating()
#         else:
#             return self.score > other.score
#
#     def __str__(self):
#         if self.matches_chronologic:
#             return str("%s (%s)" % (
#                 self.nick,
#                 self.player_rating(as_int=True)
#             ))
#         else:
#             return self.nick
#
#=========================================================================

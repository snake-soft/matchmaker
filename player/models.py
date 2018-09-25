""" model for player objects """
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

from team.models import Team


class Player(AbstractUser):
    """ Player stats are long-term statistics that are not deleted """
    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

    active_community = models.ForeignKey('community.Community', on_delete=models.SET_NULL, null=True, blank=True, related_name='active_community')
    single_team = models.OneToOneField('team.Team', on_delete=models.CASCADE, null=True, blank=True)
    gamemaster = models.ManyToManyField('community.Community', blank=True, related_name='gamemasters_set')

    email = models.EmailField(null=True, blank=True)

    nick = models.CharField(
        max_length=50, verbose_name="Playername", blank=True,)

    rating = models.FloatField(
        verbose_name="Player Rating",
        default=1000,
        validators=[MinValueValidator(0.0)],
    )

    def new_result(self, goal_diff, enemy):
        """ calculate new elo """
        elo = Elo(self.rating)
        self.rating = elo.new_result(enemy.team_rating, goal_diff)
        self.save()

    @property
    def rating_as_int(self):
        """ return rating as int """
        return self.player_rating(as_int=True)

    @property
    def score(self):
        return sum([team.team_score for team in self.teams()])

    def player_rating(self, as_int=False):
        """ return player rating """
        return int(self.rating + 0.5) if as_int else self.rating

    def teams(self):
        """ return teams of this player """
        ret = Team.objects.filter(players=self.pk)
        return ret

    def get_win_draw_lose(self):
        """ returns tuple of three lists ([win], [draw], [lose]) """
        win, draw, lose = [], [], []
        for team in self.teams():
            team_results = team.get_win_draw_lose
            win += team_results[0]
            draw += team_results[1]
            lose += team_results[2]
        return win, draw, lose

    @property
    def matches_chronologic(self):
        lst_of_lsts = [team.matches_chronologic for team in self.teams()]
        return sorted([y for x in lst_of_lsts for y in x])

    def get_close_win_lose(self):
        """ returns tuple of two lists ([close win], [close lose]) """
        win, lose = [], []
        for team in self.teams():
            team_results = team.close_win_lose
            win += team_results[0]
            lose += team_results[1]
        return win, lose

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        super().save(*args, **kwargs)
        if not bool(self.pk):
            team = Team.objects.create()
            team.players.add(self)
            self.single_team = team
            self.save()

    #===========================================================================
    # def __eq__(self, other):
    #     return self.pk == other.pk
    #===========================================================================

    #===========================================================================
    # def __lt__(self, other):
    #     if not self.matches_chronologic:
    #         return False
    #     if self.player_rating() != other.player_rating():
    #         return self.player_rating() > other.player_rating()
    #     else:
    #         return self.score > other.score
    #===========================================================================

    #===========================================================================
    # def __str__(self):
    #     if self.matches_chronologic:
    #         return str("%s (%s)" % (
    #             self.nick,
    #             self.player_rating(as_int=True)
    #         ))
    #     else:
    #         return self.nick
    #===========================================================================


class Elo:
    """ Class for managing a Elo-like rating System
    to evaluate the skills of a Player
    Differences to the Original Elo-System are:
    - Goal difference is considered
    - K value calculation simplified
    """

    def __init__(self, current_elo=1000):
        self.elo = current_elo

    def new_result(self, enemy_elo, goal_diff):
        """ returns new result from existing elo and goal difference """
        exp = self.expected(enemy_elo)
        return self.new_elo(exp, goal_diff)

    def expected(self, enemy_elo):
        """ returns the excepted match result """
        return Elo._expected(self.elo, enemy_elo)

    def new_elo(self, exp, goal_diff):
        """ returns new elo from expected and goal difference """
        return Elo._new_elo(self.elo, exp, goal_diff)

    @staticmethod
    def mapper(value, range_from, range_to, limit_to=True):
        """ maps value from range(min_from-max_from) to (min_to-max_to)
        :param value: value to map
        :param range_from: (min_from, max_from)
        :param range_to: (min_to, max_to)
        :param limit_to: False if value can be out of range
        """
        min_from, max_from = range_from
        min_to, max_to = range_to
        ret = min_to + (max_to - min_to) * ((value - min_from) /
                                            (max_from - min_from))
        if limit_to:
            if ret < min(min_to, max_to):
                ret = min(min_to, max_to)
            elif ret > max(max_to, min_to):
                ret = max(max_to, min_to)
        return ret

    @staticmethod
    def _expected(player_a, player_b):
        """ Calculate expected score of A in a match against B
        :param player_a: Elo rating for player A
        :param player_b: Elo rating for player B
        """
        if player_b - player_a < -400:
            dif = -400
        if player_b - player_a > 400:
            dif = 400
        else:
            dif = player_b - player_a
        return 1 / (1 + 10 ** ((dif) / 400))

    @staticmethod
    def _new_elo(old, exp, goal_diff):
        """ Calculate the new Elo rating for a player
        :param old: The previous Elo rating
        :param exp: The expected score for this match
        :param goal_diff: Goal difference
        """
        # Original score: win 1, draw 0.5, lose 0
        score = 0.5 + goal_diff / 10

        # Original k: default->20, elo>2400->10, less30matches->40, <18yo->40
        # Here k is mapped to the range of possible k-values (40-10)
        k = Elo.mapper(old, (0, 2400), (40, 10))
        new_elo = old + k * (score - exp)
        return new_elo if new_elo >= 0 else 0

    def __str__(self):
        ''' I love chess but against hard enemys my brain hurts '''
        return str(int(self.elo + 0.5))

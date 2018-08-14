from django.db import models
from django.core.validators import MinValueValidator


class Player(models.Model):
    nick = models.CharField(max_length=50, verbose_name="Nickname")

    rating = models.FloatField(
        verbose_name="Player Rating",
        default=1000,
        validators=[MinValueValidator(0.0)],
        )

    def get_player_rating(self):
        return self.rating

    def __str__(self):
        return str("%s (Player Rating: %s)" % (
            self.nick,
            self.get_player_rating()
            ))


class Elo:
    def __init__(self):
        self.elo = 1000

    def new_result(self, enemy_elo, goal_diff):
        exp = self.expected(enemy_elo)
        self.new_elo(exp, goal_diff)

    def expected(self, enemy_elo):
        return __class__._expected(self.elo, enemy_elo)

    def new_elo(self, exp, goal_diff):
        self.elo = __class__._new_elo(self.elo, exp, goal_diff)

    @staticmethod
    def mapper(value, minFrom, maxFrom, minTo, maxTo):
        return minTo + (maxTo - minTo) * ((value - minFrom) /
                                          (maxFrom - minFrom))

    @staticmethod
    def _expected(A, B):
        """ Calculate expected score of A in a match against B
        :param A: Elo rating for player A
        :param B: Elo rating for player B
        """
        return 1 / (1 + 10 ** ((B - A) / 400))

    @staticmethod
    def _new_elo(old, exp, goal_diff):
        """ Calculate the new Elo rating for a player
        :param old: The previous Elo rating
        :param exp: The expected score for this match
        :param goal_diff: Goal difference
        """
        if goal_diff == 0:
            score = 0.5  # normally not possible
        elif goal_diff < 0:
            score = 0 + goal_diff
        else:
            score = 1 + goal_diff / 10

        k = __class__.mapper(old, 0, 2400, 40, 10)
        return old + k * (score - exp)

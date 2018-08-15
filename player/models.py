from django.db import models
from django.core.validators import MinValueValidator


class Player(models.Model):
    """ Player stats are long-term statistics that are not deleted """
    nick = models.CharField(max_length=50, verbose_name="Nickname")

    rating = models.FloatField(
        verbose_name="Player Rating",
        default=1000,
        validators=[MinValueValidator(0.0)],
        )

    def new_result(self, goal_diff, enemy):
        elo = Elo(self.rating)
        self.rating = elo.new_result(enemy.get_team_rating(), goal_diff)
        self.save()

    def get_games_played(self):
        return 1

    def get_player_rating(self):
        return self.rating

    def __str__(self):
        return str("%s (Player Rating: %s)" % (
            self.nick,
            int(self.get_player_rating() + 0.5)
            ))


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
        exp = self.expected(enemy_elo)
        return self.new_elo(exp, goal_diff)

    def expected(self, enemy_elo):
        return __class__._expected(self.elo, enemy_elo)

    def new_elo(self, exp, goal_diff):
        self.elo = __class__._new_elo(self.elo, exp, goal_diff)
        return self.elo

    @staticmethod
    def mapper(value, minFrom, maxFrom, minTo, maxTo, limitTo=True):
        ret = minTo + (maxTo - minTo) * ((value - minFrom) /
                                         (maxFrom - minFrom))
        if limitTo:
            if ret < min(minTo, maxTo):
                ret = min(minTo, maxTo)
            elif ret > max(maxTo, minTo):
                ret = max(maxTo, minTo)
        return ret

    @staticmethod
    def _expected(A, B):
        """ Calculate expected score of A in a match against B
        :param A: Elo rating for player A
        :param B: Elo rating for player B
        """
        if B-A < -400:
            dif = -400
        if B-A > 400:
            dif = 400
        else:
            dif = B-A
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
        k = __class__.mapper(old, 0, 2400, 40, 10)
        return old + k * (score - exp)

    def __str__(self):
        ''' I love chess but against hard enemys my brain hurts '''
        return str(int(self.elo + 0.5))

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


def expected(A, B):
    """ Calculate expected score of A in a match against B
    :param A: Elo rating for player A
    :param B: Elo rating for player B
    """
    return 1 / (1 + 10 ** ((B - A) / 400))


def elo(old, exp, score, counted_games):
    """ Calculate the new Elo rating for a player
    :param old: The previous Elo rating
    :param exp: The expected score for this match
    :param score: Goal difference
    """
    if score <= 0:
        score = 0
    else:
        score = 1 + score / 10

    if old > 2400:
        k = 10
    elif counted_games < 40:
        k = 40
    else:
        k = 20  # default

    return old + k * (score - exp)
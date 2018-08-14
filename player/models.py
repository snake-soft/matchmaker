from django.db import models


class Player(models.Model):
    nick = models.CharField(max_length=50, verbose_name="Nickname")

    pscore = models.PositiveIntegerField(
        verbose_name="Player Score",
        default=1000
        )

    def get_player_score(self):
        return self.pscore

    def __str__(self):
        return str("%s (Player Score: %s)" % (
            self.nick,
            self.get_player_score()
            ))

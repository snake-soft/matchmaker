from django.db import models


class Player(models.Model):
    nick = models.CharField(max_length=50, verbose_name="Nickname")

    def get_player_score(self):
        return 1

    def __str__(self):
        return str("%s" % (self.nick))

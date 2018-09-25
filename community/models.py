from django.db import models
from django.conf import settings


class Community(models.Model):
    class Meta:
        verbose_name = "Community"
        verbose_name_plural = "Community"

    name = models.CharField(max_length=50, verbose_name="Community Name")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    @property
    def gamemasters(self):
        ret = list(self.gamemasters_set.all())
        if self.creator:
            ret.append(self.creator)
        return ret

    @property
    def players(self):
        lst = [x.players.all() for x in self.teams]
        import pdb; pdb.set_trace()  # <---------

    @property
    def teams(self):
        return self.team_set.all()

    def __str__(self):
        return self.name

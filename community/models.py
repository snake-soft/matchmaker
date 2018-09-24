from django.db import models


class Community(models.Model):
    class Meta:
        verbose_name = "Community"
        verbose_name_plural = "Community"

    name = models.CharField(max_length=50, verbose_name="Community Name")
    gamemaster = models.ManyToManyField('player.Player')

    @property
    def players(self):
        import pdb; pdb.set_trace()  # <---------
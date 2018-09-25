from django.db import models


class CommunityMembership(models.Model):
    member = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    community = models.ForeignKey('community.Community',
                                  on_delete=models.CASCADE)
    owner = models.BooleanField(default=False)
    gamemaster = models.BooleanField(default=False)

    class Meta:
        unique_together = ('member', 'community')


class Community(models.Model):
    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

    name = models.CharField(max_length=50, verbose_name="Name", blank=True)

    @property
    def gamemasters(self):
        import pdb; pdb.set_trace()  # <---------
        return 

    @property
    def players(self):
        return self.player_set.all()

    @property
    def teams(self):
        return self.team_set.all()

    def __str__(self):
        return self.name

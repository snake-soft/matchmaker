from django.db import models


class CommunityMembership(models.Model):
    member = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    community = models.ForeignKey('community.Community',
                                  on_delete=models.CASCADE)
    owner = models.BooleanField(default=False)
    gamemaster = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)  # FUTURE

    def __str__(self):
        return str(self.member)

    class Meta:
        unique_together = ('member', 'community')


class Community(models.Model):

    name = models.CharField(max_length=50, verbose_name="Name", blank=True)

    @property
    def gamemasters(self):
        return self.communitymembership_set.filter(owner=True)

    @property
    def players(self):
        return self.player_set.all()

    @property
    def teams(self):
        return self.team_set.all()

    def set_players(self, playerlist):

        def list_compare(old, new):
            """ return{'rem':[miss in new], 'add':[miss in old]} """
            return {
                'rem': [x for x in old if x not in new],
                'add': [x for x in new if x not in old]
                }

        result = list_compare(self.players, playerlist)
        for player in result['add']:
            self.communitymembership_set.create(member=player)

        for player in result['rem']:
            [x.delete() for x in self.communitymembership_set.all()
             if not x.owner and not x.gamemaster]

    def __str__(self):
        print(self.gamemasters)
        return self.name

    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

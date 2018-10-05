from django.db import models
from django.contrib.auth.models import Group, GroupManager
from core.shared import list_compare


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
    def owner(self):
        return [x.member for x in self.communitymembership_set.filter(
            owner=True)]

    @property
    def gamemasters(self):
        return [x.member for x in self.communitymembership_set.filter(
            gamemaster=True)]

    @property
    def players(self):
        return self.player_set.all()

    @property
    def teams(self):
        return self.team_set.all()

    def is_community_admin(self, player):
        return player in self.gamemasters or player in self.owner

    def remove_player(self, member):
        if member in self.players:
            [x.delete() for x in self.communitymembership_set.filter(
                member=member) if not x.owner]

    def add_player(self, member):
        if member not in self.players:
            self.communitymembership_set.create(member=member).save()

    def set_players(self, playerlist):
        result = list_compare(self.players, playerlist)
        for member in result['add']:
            self.add_player(member)
        for member in result['rem']:
            self.remove_player(member)

    def remove_gamemaster(self, member):
        if member in self.gamemasters:
            membership = self.communitymembership_set.get(member=member)
            membership.gamemaster = False
            membership.save()

    def add_gamemaster(self, member):
        if member not in self.gamemasters:
            membership = self.communitymembership_set.get(member=member)
            membership.gamemaster = True
            membership.save()

    def set_gamemasters(self, gmlist):
        result = list_compare(self.gamemasters, gmlist)
        print(result)
        for member in result['add']:
            self.add_gamemaster(member)
        for member in result['rem']:
            self.remove_gamemaster(member)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'

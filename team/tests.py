from django.test import TestCase
from datetime import date

from .models import Team
from player.models import Player


class TeamTestCase(TestCase):
    def setUp(self):
        self.frank = Player.objects.create(nick="Frank")
        self.alex = Player.objects.create(nick="Alexandra")
        self.sebi = Player.objects.create(nick="Sebastiano")
        self.uenal = Player.objects.create(nick="Ünal")

        self.devils = Team.objects.create(teamname="Devils")
        self.devils.players.add(self.frank)
        self.devils.players.add(self.sebi)

        self.dimension = Team.objects.create(teamname="Dimension")
        self.dimension.players.add(self.frank)
        self.dimension.players.add(self.alex)

        self.single_team = Team.objects.get(teamname="Frank")

    def test_set_from_to(self):
        frm = self.devils.frm
        to = self.devils.to
        self.devils.set_from_to(date(2018,1,1), date(2018,12,31))
        if frm is self.devils.frm or to is self.devils.to:
            raise ValueError("Time not setted correctly")

    def test_team_score(self):
        if type(self.devils.team_score) is not int:
            raise ValueError(self)

        
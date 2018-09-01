from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Match
from team.models import Team
from player.models import Player


class MatchModelsTestCase(TestCase):
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

        self.match1 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank"),
            secondteam=Team.objects.get(teamname="Alexandra"),
            firstteam_goals=10,
            secondteam_goals=5,
            )
        self.match2 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank"),
            secondteam=Team.objects.get(teamname="Alexandra"),
            firstteam_goals=5,
            secondteam_goals=10,
            )

    def test_goal_difference(self):
        self.assertEquals(type(self.match1.goal_difference), int)

    def test_rematches(self):
        self.assertEquals(type(self.match1.rematches), list)
        self.assertTrue(len(self.match1.rematches) >= 1)

    def test_save(self):
        with self.assertRaises(ValidationError):
            self.match3 = Match.objects.create(
                firstteam=Team.objects.get(teamname="Frank"),
                secondteam=Team.objects.get(teamname="Frank"),
                firstteam_goals=5,
                secondteam_goals=10,
                )

    def test_str(self):
        self.assertEquals(type(str(Match.objects.all()[0])), str)

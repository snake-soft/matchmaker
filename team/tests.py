from django.test import TestCase
from datetime import date

from .models import Team
from player.models import Player
from match.models import Match
from . import apps


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)


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

        self.nameless_team = Team.objects.create()
        self.nameless_team.players.add(self.frank)
        self.nameless_team.players.add(self.alex)

        self.empty_team = Team.objects.create(teamname="Empty")

        self.single_team = Team.objects.get(teamname="Frank")

        Match.objects.create(
            firstteam=self.devils,
            secondteam=self.dimension,
            firstteam_goals=5,
            secondteam_goals=5,
            )
        Match.objects.create(
            firstteam=self.dimension,
            secondteam=self.devils,
            firstteam_goals=5,
            secondteam_goals=5,
            )
        Match.objects.create(
            firstteam=self.dimension,
            secondteam=self.devils,
            firstteam_goals=5,
            secondteam_goals=6,
            )
        Match.objects.create(
            firstteam=self.dimension,
            secondteam=self.devils,
            firstteam_goals=6,
            secondteam_goals=5,
            )

    def test_set_from_to(self):
        frm = self.devils.frm
        to = self.devils.to
        self.devils.set_from_to(date(2018, 1, 1), date(2018, 12, 31))
        self.assertFalse(frm is self.devils.frm or to is self.devils.to)

    def test_team_score(self):
        self.assertEqual(type(self.devils.team_score), int)

    def test_team_rating(self):
        self.assertEqual(type(self.dimension.team_rating), float)
        self.assertEqual(type(self.empty_team.team_rating), float)

    def test_verbose_name(self):
        self.assertEqual(type(self.empty_team.verbose_name), str)

    def test_team_rating_as_int(self):
        self.assertEqual(type(self.empty_team.team_rating_as_int), int)

    def test_get_team_name_or_members(self):
        self.assertEqual(
            type(self.nameless_team.get_team_name_or_members()),
            str
            )

    def test_win_draw_lose(self):
        self.assertEqual(type(self.dimension.team_win[0]), Match)
        self.assertEqual(type(self.dimension.team_draw[0]), Match)
        self.assertEqual(type(self.dimension.team_lose[0]), Match)
        self.assertEqual(type(self.dimension.close_wl_factor), int)

    def test_close_win_lose(self):
        self.assertEqual(type(self.dimension.close_win[0]), Match)
        self.assertEqual(type(self.dimension.close_lose[0]), Match)
        self.assertEqual(type(self.devils.close_win[0]), Match)
        self.assertEqual(type(self.devils.close_lose[0]), Match)

    def test_goal_own_foreign(self):
        self.assertEqual(type(self.dimension.goal_own), int)
        self.assertEqual(type(self.dimension.goal_foreign), int)
        self.assertEqual(type(self.dimension.goal_factor), int)
        self.assertEqual(type(self.empty_team.goal_factor), int)

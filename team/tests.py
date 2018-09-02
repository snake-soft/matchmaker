from django.test import TestCase, Client
from django.shortcuts import reverse
from datetime import date

from .models import Team
from player.models import Player
from match.models import Match
from . import apps


class TeamViewsTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.frank = Player.objects.create(nick="Frank")
        self.alex = Player.objects.create(nick="Alexandra")

    def test_list_realtime(self):
        post_data = {'from': '2018-01-01', 'to': '2020-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        self.assertRedirects(response, post_data['next'], 302)

        get_data = {
            'firstteam': 1,
            'secondteam': 2,
            'firstteam_goals': 1,
            'secondteam_goals': 2,
            }
        response = self.client.get(reverse('team-realtime'), get_data)
        self.assertTemplateUsed(response, 'team/team_list_realtime.html')

        get_data = {
            'firstteam': 1,
            'secondteam': 2,
            'firstteam_goals': 2,
            'secondteam_goals': 2,
            }
        response = self.client.get(reverse('team-realtime'), get_data)
        self.assertTemplateUsed(response, 'team/team_list_realtime.html')

    def test_team_create(self):
        post_data = {'from': '2018-01-01', 'to': '2020-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        self.assertRedirects(response, post_data['next'], 302)

        post_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertEqual(response.status_code, 302)

        get_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.get(reverse('team-new'), get_data)
        self.assertEqual(response.status_code, 200)


class TeamModelsTestCase(TestCase):
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

        self.single_name = Team.objects.create(teamname="SingleName")
        self.single_name.players.add(self.frank)

        #=======================================================================
        # with self.assertRaises(ValueError):
        #     self.single_name = Team.objects.create(teamname="SingleName")
        #=======================================================================

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

    def test_is_player_team(self):
        self.assertEqual(type(self.single_name.is_player_team), str)
        self.assertEqual(self.dimension.is_player_team, False)
        self.assertEqual(self.single_team.is_player_team, True)


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)

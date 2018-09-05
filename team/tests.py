from django.test import TestCase
from django.shortcuts import reverse
from datetime import date

from config.tests import TestBase
from match.models import Match
from . import apps
from .models import Team


class TeamViewsTestCase(TestCase):
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_team_details(self):
        response = self.client.get(
            reverse('team-details', args=[Team.objects.all()[0].pk])
        )
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/team_detail.html')
        self.assertIn(
            str(Team.objects.all()[0].teamname), response.rendered_content)

    def test_team_list(self):
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/team_list.html')
        post_data = {'from': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/team_list.html')

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
        self.assertIs(response.context, None)
        self.assertRedirects(response, post_data['next'], 302)

        post_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIn('error', response.context['form'].errors)
        self.assertEqual(response.status_code, 200)

        post_data = {'teamname': 'CreatedTeam', 'players': ['3', '2']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIs(response.context, None)
        self.assertEqual(response.status_code, 302)

        get_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.get(reverse('team-new'), get_data)
        self.assertNotIn('error', response.context['form'].errors)
        self.assertEqual(response.status_code, 200)

        post_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIn('error', response.context['form'].errors)
        self.assertEqual(response.status_code, 200)

        post_data = {'teamname': 'CreatedTeam', 'players': ['3', '4']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIn('error', response.context['form'].errors)
        self.assertEqual(response.status_code, 200)


class TeamModelsTestCase(TestCase):
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_set_from_to(self):
        frm = self.db.devils.frm
        to = self.db.devils.to
        self.db.devils.set_from_to(date(2018, 1, 1), date(2018, 12, 31))
        self.assertFalse(frm is self.db.devils.frm or to is self.db.devils.to)

    def test_team_score(self):
        self.assertEqual(type(self.db.devils.team_score), int)

    def test_team_rating(self):
        self.assertEqual(type(self.db.dimension.team_rating), float)
        self.assertEqual(type(self.db.empty_team.team_rating), float)

    def test_verbose_name(self):
        self.assertEqual(type(self.db.empty_team.verbose_name), str)

    def test_team_rating_as_int(self):
        self.assertEqual(type(self.db.empty_team.team_rating_as_int), int)

    def test_get_team_name_or_members(self):
        self.assertEqual(
            type(self.db.nameless_team.get_team_name_or_members()),
            str
        )

    def test_win_draw_lose(self):
        self.assertEqual(type(self.db.dimension.team_win[0]), Match)
        self.assertEqual(type(self.db.dimension.team_draw[0]), Match)
        self.assertEqual(type(self.db.dimension.team_lose[0]), Match)
        self.assertEqual(type(self.db.dimension.close_wl_factor), int)

    def test_close_win_lose(self):
        self.assertEqual(type(self.db.dimension.close_win[0]), Match)
        self.assertEqual(type(self.db.dimension.close_lose[0]), Match)
        self.assertEqual(type(self.db.devils.close_win[0]), Match)
        self.assertEqual(type(self.db.devils.close_lose[0]), Match)

    def test_goal_own_foreign(self):
        self.assertEqual(type(self.db.dimension.goal_own), int)
        self.assertEqual(type(self.db.dimension.goal_foreign), int)
        self.assertEqual(type(self.db.dimension.goal_factor), int)
        self.assertEqual(type(self.db.empty_team.goal_factor), int)

    def test_is_player_team(self):
        self.assertEqual(self.db.dimension.is_player_team, False)
        self.assertEqual(self.db.single_team.is_player_team, True)


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)

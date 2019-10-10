""" tests for team module """
from datetime import date

from django.test import TestCase
from django.shortcuts import reverse

from config.tests import TestBase
from match.models import Match
from . import apps
from .models import Team


class TeamViewsTestCase(TestCase):
    """ team views tests """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_team_details(self):
        """ test team details view """
        response = self.client.get(
            reverse('team-details', args=[Team.objects.all()[0].pk])
        )
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/team_detail.html')
        self.assertIn("<div", response.rendered_content)

    def test_team_list(self):
        """ test team list view """
        response = self.client.get(reverse('team-list'))
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/team_list.html')
        post_data = {'from': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        response = self.client.get(reverse('team-list'))
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'team/team_list.html')

    def test_list_realtime(self):
        """ test realtime list """
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
        """ test team create view """
        post_data = {'from': '2018-01-01', 'to': '2020-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        self.assertIs(response.context, None)
        self.assertRedirects(response, post_data['next'], 302)

        post_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIn('error', response.context['form'].errors)
        self.assertIs(response.status_code, 200)

        post_data = {'teamname': 'CreatedTeam', 'players': ['3', '2']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIs(response.context, None)

        self.assertRedirects(response, "/ladder/", 302)
        get_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.get(reverse('team-new'), get_data)
        self.assertNotIn('error', response.context['form'].errors)
        self.assertIs(response.status_code, 200)

        post_data = {'teamname': 'CreatedTeam', 'players': ['1', '2']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIn('error', response.context['form'].errors)
        self.assertIs(response.status_code, 200)

        post_data = {'teamname': 'CreatedTeam', 'players': ['3', '4']}
        response = self.client.post(reverse('team-new'), post_data)
        self.assertIn('error', response.context['form'].errors)
        self.assertIs(response.status_code, 200)


class TeamModelsTestCase(TestCase):
    """ team model tests """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_set_from_to(self):
        """ test set_from_to """
        frm = self.db_.devils.frm
        to_ = self.db_.devils.to_
        self.db_.devils.set_from_to(date(2018, 1, 1), date(2018, 12, 31))
        self.assertFalse(
            frm is self.db_.devils.frm or to_ is self.db_.devils.to_)

    def test_team_score(self):
        """ test team_score """
        self.assertIs(type(self.db_.devils.team_score), int)

    def test_team_rating(self):
        """ test team_rating """
        self.assertIs(type(self.db_.dimension.team_rating), float)
        self.assertIs(type(self.db_.empty_team.team_rating), float)

    def test_verbose_name(self):
        """ test verbose_name """
        self.assertIs(type(self.db_.empty_team.verbose_name), str)

    def test_team_rating_as_int(self):
        """ test team_rating_as_int """
        self.assertIs(type(self.db_.empty_team.team_rating_as_int), int)

    def test_get_team_name_or_members(self):
        """ test get_team_name_or_members """
        self.assertIs(
            type(self.db_.nameless_team.get_team_name_or_members()), str)

    # ==========================================================================
    # def test_win_draw_lose(self):
    #     """ test win_draw_lose """
    #     wdl = self.db_.dimension.get_win_draw_lose
    #     self.assertIsInstance(wdl[0][0], Match)
    #     self.assertIsInstance(wdl[1][0], Match)
    #     self.assertIsInstance(wdl[2][0], Match)
    #     self.assertIsInstance(self.db_.dimension.close_wl_factor, int)
    # ==========================================================================

    def test_close_win_lose(self):
        """ test close_win_lose """
        self.assertIs(type(self.db_.dimension.close_win_lose[0][0]), Match)
        self.assertIs(type(self.db_.dimension.close_win_lose[1][0]), Match)
        self.assertIs(type(self.db_.devils.close_win_lose[0][0]), Match)
        self.assertIs(type(self.db_.devils.close_win_lose[1][0]), Match)

    def test_goal_own_foreign(self):
        """ test goal_own_foreign """
        self.assertIs(type(self.db_.dimension.goal_own_foreign[0]), int)
        self.assertIs(type(self.db_.dimension.goal_own_foreign[1]), int)
        self.assertIs(type(self.db_.dimension.goal_factor), int)
        self.assertIs(type(self.db_.empty_team.goal_factor), int)

    def test_is_player_team(self):
        """ test is_player_team """
        self.assertIs(self.db_.dimension.is_player_team, False)
        self.assertIs(self.db_.single_team.is_player_team, True)


class AppsTestCase(TestCase):
    """ test core apps config """

    def test_apps(self):
        """ checkt type """
        self.assertIs(type(apps.AppConfig), type)

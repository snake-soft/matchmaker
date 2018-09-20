""" Tests for match module """
from django.test import TestCase
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

from config.tests import TestBase
from team.models import Team
from .models import Match
from . import apps


class MatchViewsTestCase(TestCase):
    """ Tests for Match views """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_match_details(self):
        """ tests match detail view """
        post_data = {'frm': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        self.client.post(reverse('set-date'), post_data)
        response = self.client.get(
            reverse('match-details', args=[Match.objects.all()[0].pk])
        )
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'match/match_detail.html')
        self.assertIn(
            str(Match.objects.all()[0].firstteam), response.rendered_content)

    def test_match_list(self):
        """ test match list view """
        response = self.client.get(reverse('match-list'))
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'match/match_list.html')
        post_data = {'frm': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        response = self.client.get(reverse('match-list'))
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'match/match_list.html')

    def test_match_create(self):
        """ test creation of new match """
        get_data = {
            'firstteam': '1',
            'secondteam': '2',
            'firstteam_goals': '10',
            'secondteam_goals': '5',
        }
        response = self.client.get(reverse('match-new'), get_data)
        self.assertTemplateUsed(response, 'match/match_form.html')

        post_data = {
            'firstteam': '1',
            'secondteam': '2',
            'firstteam_goals': '10',
            'secondteam_goals': '5',
        }
        response = self.client.post(reverse('match-new'), post_data)
        self.assertRedirects(response, reverse('match-new'), 302)

        post_data = {
            'firstteam': '1',
            'secondteam': '2',
            'firstteam_goals': '5',
            'secondteam_goals': '10',
        }
        response = self.client.post(reverse('match-new'), post_data)
        self.assertRedirects(response, reverse('match-new'), 302)

        post_data = {
            'firstteam': '1',
            'secondteam': '2',
            'firstteam_goals': '5',
            'secondteam_goals': '5',
        }
        response = self.client.post(reverse('match-new'), post_data)
        self.assertRedirects(response, reverse('match-new'), 302)

        post_data = {
            'firstteam': '1',
            'secondteam': '2',
            'firstteam_goals': '0',
            'secondteam_goals': '0',
        }
        response = self.client.post(reverse('match-new'), post_data)
        self.assertTemplateUsed(response, 'match/match_form.html')
        self.assertIn('error', response.context['form'].errors)

        post_data = {
            'firstteam': '1',
            'secondteam': '1',
            'firstteam_goals': '10',
            'secondteam_goals': '5',
        }
        response = self.client.post(reverse('match-new'), post_data)
        self.assertTemplateUsed(response, 'match/match_form.html')
        self.assertIn('error', response.context['form'].errors)

        post_data = {
            'secondteam': '1',
            'firstteam_goals': '10',
            'secondteam_goals': '5',
        }
        response = self.client.post(reverse('match-new'), post_data)
        self.assertTemplateUsed(response, 'match/match_form.html')
        self.assertIn('firstteam', response.context['form'].errors)


class DateSetViewTestCase(TestCase):
    """ Tests setting new date """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_post(self):
        """ set new date """
        post_data = {'from': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        self.assertRedirects(response, post_data['next'], 302)


class MatchModelsTestCase(TestCase):
    """ Tests match model (most methods are tested by views above) """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_goal_difference(self):
        """ test goal difference """
        self.assertIs(type(self.db_.match1.goal_difference), int)

    def test_rematches(self):
        """ test rematches """
        self.assertIs(type(self.db_.match1.rematches), list)
        self.assertTrue(len(self.db_.match1.rematches) >= 1)

    def test_save(self):
        """ test save method """
        with self.assertRaises(ValidationError):
            Match.objects.create(
                firstteam=Team.objects.get(teamname="Frank"),
                secondteam=Team.objects.get(teamname="Frank"),
                firstteam_goals=5,
                secondteam_goals=10,
            )

    def test_str(self):
        """ test str method """
        self.assertIs(type(str(Match.objects.all()[0])), str)


class AppsTestCase(TestCase):
    """ core apps config """

    def test_apps(self):
        """ checkt type """
        self.assertIs(type(apps.AppConfig), type)

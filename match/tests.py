from django.test import TestCase
from django.shortcuts import reverse
from django.core.exceptions import ValidationError

from config.tests import TestBase
from .models import Match
from . import apps
from team.models import Team


class MatchViewsTestCase(TestCase):

    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_match_details(self):
        response = self.client.get(
            reverse('match-details', args=[Match.objects.all()[0].pk])
        )
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'match/match_detail.html')
        self.assertIn(
            str(Match.objects.all()[0].firstteam), response.rendered_content)

    def test_match_list(self):
        response = self.client.get(reverse('match-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'match/match_list.html')
        post_data = {'frm': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        response = self.client.get(reverse('match-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'match/match_list.html')

    def test_match_create(self):
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
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_post(self):
        post_data = {'from': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        self.assertRedirects(response, post_data['next'], 302)


class MatchModelsTestCase(TestCase):

    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_goal_difference(self):
        self.assertEquals(type(self.db.match1.goal_difference), int)

    def test_rematches(self):
        self.assertEquals(type(self.db.match1.rematches), list)
        self.assertTrue(len(self.db.match1.rematches) >= 1)

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


class AppsTestCase(TestCase):

    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)

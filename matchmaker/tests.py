""" tests for matchmaker module """
from django.shortcuts import reverse
from django.test import TestCase

from config.tests import TestBase
from . import apps
from .models import ConstellationFactory, Constellation


class MatchmakerModelTestCase(TestCase):
    """ Test for matchmaker model """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_constellation_factory(self):
        """ test constellation factory """
        factory = ConstellationFactory([self.db_.frank, self.db_.alex], 2)
        constellation = factory.get_constellations()[0]
        self.assertIs(type(constellation), Constellation)
        self.assertIs(type(constellation.team1.player_ids[0]), int)


class MatchmakerViewTestCase(TestCase):
    """ Tests for matchmaker views  """

    def setUp(self):
        """ setup MatchmakerViewTestCase """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_get(self):
        """ test get method """
        get_data = {}
        post_data = {'frm': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        self.client.post(reverse('set-date'), post_data)
        response = self.client.get(reverse('matchmaker'), get_data)
        self.assertTemplateUsed(response, 'matchmaker/matchmaker_form.html')

        get_data = {'players': [1, 2], 'count': 2, }
        response = self.client.get(reverse('matchmaker'), get_data)
        self.assertTemplateUsed(response, 'matchmaker/matchmaker_form.html')

        get_data = {'players': [1, 2], 'count': 3, }
        response = self.client.get(reverse('matchmaker'), get_data)
        self.assertTemplateUsed(response, 'matchmaker/matchmaker_form.html')
        self.assertIn('error', response.context['matchmaker_form'].errors)

    def test_post(self):
        """ test post method """
        post_data = {'last_players': [1, 2], 'count': 2}
        self.client.post(reverse('matchmaker'), post_data)


class AppsTestCase(TestCase):
    """ core apps config """

    def test_apps(self):
        """ checkt type """
        self.assertIs(type(apps.AppConfig), type)

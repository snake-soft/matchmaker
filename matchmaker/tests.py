from django.shortcuts import reverse
from django.test import TestCase

from config.tests import TestBase
from . import apps
from .models import ConstellationFactory, Constellation


class MatchmakerModelTestCase(TestCase):
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_constellation_factory(self):
        cf = ConstellationFactory([self.db.frank, self.db.alex], 2)
        constellation = cf.get_constellations()[0]
        self.assertEqual(type(constellation), Constellation)
        self.assertEqual(type(constellation.team1.player_ids[0]), int)


class MatchmakerViewTestCase(TestCase):
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_get(self):
        get_data = {
            'players': [1, 2],
            'count': 2,
        }
        response = self.client.get(reverse('matchmaker'), get_data)
        self.assertTemplateUsed(response, 'matchmaker/matchmaker_form.html')

    def test_post(self):
        post_data = {'last_players': [1, 2], 'count': 2}
        _ = self.client.post(reverse('matchmaker'), post_data)


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)

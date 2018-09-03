from django.shortcuts import reverse
from django.test import TestCase
from django.test.client import Client

from team.models import Team
from player.models import Player
from . import apps
from .models import ConstellationFactory, Constellation


class MatchmakerModelTestCase(TestCase):
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

    def test_constellation_factory(self):
        cf = ConstellationFactory([self.frank, self.alex], 2)
        constellation = cf.get_constellations()[0]
        self.assertEqual(type(constellation), Constellation)
        self.assertEqual(type(constellation.team1.player_ids[0]), int)


class MatchmakerViewTestCase(TestCase):
    client = Client()

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

    def test_get(self):
        get_data = {
            'players': [1, 2],
            'count': 2,
            }
        response = self.client.get(reverse('matchmaker'), get_data)
        self.assertTemplateUsed(response, 'matchmaker/matchmaker_form.html')

    def test_post(self):
        post_data = {'last_players': [1, 2], 'count': 2}
        response = self.client.post(reverse('matchmaker'), post_data)
        import pdb; pdb.set_trace()  # <---------import pdb; pdb.set_trace()  # <---------


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)

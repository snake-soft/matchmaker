from django.test import TestCase
from django.shortcuts import reverse

from config.tests import TestBase
from team.models import Team
from match.models import Match
from . import apps
from .models import Player, Elo


class PlayerViewsTestCase(TestCase):
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_player_details(self):
        response = self.client.get(
            reverse('player-details', args=[Player.objects.all()[0].pk])
        )
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/player_detail.html')
        self.assertIn(
            str(Player.objects.all()[0].nick), response.rendered_content)

    def test_match_list(self):
        response = self.client.get(reverse('player-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/player_list.html')
        post_data = {'from': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        response = self.client.get(reverse('player-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/player_list.html')

    def test_player_create(self):
        post_data = {
            'nick': 'Hanswurst',
        }
        response = self.client.post(reverse('player-new'), post_data)
        self.assertRedirects(response, reverse('ladder'), 302)

        post_data = {
            'nick': 'Hanswurst',
        }
        response = self.client.post(reverse('player-new'), post_data)
        self.assertIs(response.status_code, 200)
        self.assertIn('error', response.context['form'].errors)

        response = self.client.get(reverse('player-new'))
        self.assertTemplateUsed(response, 'player/player_form.html')


class PlayerModelTestCase(TestCase):
    def setUp(self):
        tb = TestBase()
        self.client = tb.client
        self.db = tb.db

    def test_get_teams(self):
        self.assertEqual(type(self.db.frank.teams()[0]), Team)

    def test_get_win_draw_lose(self):
        wdl = self.db.frank.get_win_draw_lose()
        self.assertEqual(type(wdl[0][0]), Match)
        self.assertEqual(type(wdl[2][0]), Match)

    def test_save(self):
        with self.assertRaises(ValueError):
            Player.objects.create(nick="Frank", owner=self.db.me)
        with self.assertRaises(ValueError):
            Player.objects.create(nick="Devils", owner=self.db.me)

    def test_str(self):
        self.assertEqual(type(str(self.db.frank)), str)

    def test_elo(self):
        elo = Elo(1000)
        elo.mapper(-10, 0, 100, 0, 1000, True)
        elo.mapper(1000, 0, 100, 0, 1000, True)
        elo.expected(100)
        elo.expected(10000)
        self.assertEqual(type(str(elo)), str)


class AppsTestCase(TestCase):
    def test_apps(self):
        self.assertEqual(type(apps.AppConfig), type)

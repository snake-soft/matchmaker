""" tests for player module """
from django.test import TestCase
from django.shortcuts import reverse

from config.tests import TestBase
from team.models import Team
from match.models import Match
from . import apps
from .models import Player, Elo


class PlayerViewsTestCase(TestCase):
    """ player views tests """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_player_details(self):
        """ test player details view """
        response = self.client.get(
            reverse('player-details', args=[Player.objects.all()[0].pk])
        )
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/player_detail.html')
        self.assertIn(
            str(Player.objects.all()[0].nick), response.rendered_content)

    def test_match_list(self):
        """ test match list view """
        response = self.client.get(reverse('player-list'))
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/player_list.html')
        post_data = {'from': '2018-01-01', 'to': '2018-01-31', 'next': '/'}
        response = self.client.post(reverse('set-date'), post_data)
        response = self.client.get(reverse('player-list'))
        self.assertIs(response.status_code, 200)
        self.assertTemplateUsed(response, 'player/player_list.html')

    def test_player_create(self):
        """ test player creation """
        post_data = {'nick': 'Hanswurst', }
        response = self.client.post(reverse('player-new'), post_data)
        self.assertRedirects(response, reverse('ladder'), 302)

        post_data = {'nick': 'Hanswurst', }
        response = self.client.post(reverse('player-new'), post_data)
        self.assertIs(response.status_code, 200)
        self.assertIn('error', response.context['form'].errors)

        response = self.client.get(reverse('player-new'))
        self.assertTemplateUsed(response, 'player/player_form.html')


class PlayerModelTestCase(TestCase):
    """ player model tests """

    def setUp(self):
        """ setup """
        testbase = TestBase()
        self.client = testbase.client
        self.db_ = testbase.db_

    def test_get_teams(self):
        """ test teams get method """
        self.assertIs(type(self.db_.frank.teams()[0]), Team)

    def test_get_win_draw_lose(self):
        """ test get win draw lose """
        wdl = self.db_.frank.get_win_draw_lose()
        self.assertIs(type(wdl[0][0]), Match)
        self.assertIs(type(wdl[2][0]), Match)

    def test_save(self):
        """ test save method """
        with self.assertRaises(ValueError):
            Player.objects.create(nick="Frank", owner=self.db_.me_)
        with self.assertRaises(ValueError):
            Player.objects.create(nick="Devils", owner=self.db_.me_)

    def test_str(self):
        """ test str method """
        self.assertIs(type(str(self.db_.frank)), str)

    def test_elo(self):
        """ test elo handling """
        elo = Elo(1000)
        elo.mapper(-10, (0, 100), (0, 1000), True)
        elo.mapper(1000, (0, 100), (0, 1000), True)
        elo.expected(100)
        elo.expected(10000)
        self.assertIs(type(str(elo)), str)


class AppsTestCase(TestCase):
    """ test core apps config """

    def test_apps(self):
        """ checkt type """
        self.assertIs(type(apps.AppConfig), type)

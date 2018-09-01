from django.test import TestCase, Client
from django.shortcuts import reverse

from team.models import Team
from match.models import Match
from . import apps
from .models import Player, Elo


class PlayerViewsTestCase(TestCase):
    client = Client()

    def test_player_create(self):
        post_data = {
            'nick': 'Hanswurst',
            }
        response = self.client.post(reverse('player-new'), post_data)
        self.assertRedirects(response, reverse('player-list'), 302)

        response = self.client.get(reverse('player-new'))
        self.assertTemplateUsed(response, 'player/player_form.html')


class PlayerModelTestCase(TestCase):
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

        self.match1 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank"),
            secondteam=Team.objects.get(teamname="Alexandra"),
            firstteam_goals=10,
            secondteam_goals=5,
            )
        self.match2 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank"),
            secondteam=Team.objects.get(teamname="Alexandra"),
            firstteam_goals=5,
            secondteam_goals=10,
            )

    def test_get_teams(self):
        self.assertEqual(type(self.frank.teams()[0]), Team)

    def test_get_win_draw_lose(self):
        wdl = self.frank.get_win_draw_lose()
        self.assertEqual(type(wdl[0][0]), Match)
        self.assertEqual(type(wdl[2][0]), Match)

    def test_save(self):
        with self.assertRaises(ValueError):
            Player.objects.create(nick="Frank")
        with self.assertRaises(ValueError):
            Player.objects.create(nick="Devils")

    def test_str(self):
        self.assertEqual(type(str(self.frank)), str)

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

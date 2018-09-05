from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from player.models import Player
from team.models import Team
from match.models import Match


class TestBase:
    def __init__(self):
        self.db = lambda: None  # Create Namespace
        self.client = self.create_user_and_login()
        self.create_sample_db()

    def create_sample_db(self):
        obj = self.db
        obj.frank = Player.objects.create(nick="Frank")
        obj.alex = Player.objects.create(nick="Alexandra")
        obj.sebi = Player.objects.create(nick="Sebastiano")
        obj.uenal = Player.objects.create(nick="Ünal")

        obj.devils = Team.objects.create(teamname="Devils")
        obj.devils.players.add(obj.frank)
        obj.devils.players.add(obj.sebi)

        obj.dimension = Team.objects.create(teamname="Dimension")
        obj.dimension.players.add(obj.frank)
        obj.dimension.players.add(obj.alex)

        obj.nameless_team = Team.objects.create()
        obj.nameless_team.players.add(obj.frank)
        obj.nameless_team.players.add(obj.alex)

        obj.empty_team = Team.objects.create(teamname="Empty")

        obj.single_team = Team.objects.get(teamname="Frank")

        obj.match1 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank"),
            secondteam=Team.objects.get(teamname="Alexandra"),
            firstteam_goals=10,
            secondteam_goals=5,
        )
        obj.match2 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank"),
            secondteam=Team.objects.get(teamname="Alexandra"),
            firstteam_goals=5,
            secondteam_goals=10,
        )

        obj.single_name = Team.objects.create(teamname="SingleName")
        obj.single_name.players.add(obj.frank)

        Match.objects.create(
            firstteam=obj.devils,
            secondteam=obj.dimension,
            firstteam_goals=5,
            secondteam_goals=5,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=5,
            secondteam_goals=5,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=5,
            secondteam_goals=6,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=6,
            secondteam_goals=5,
        )

    def create_user_and_login(self):
        self.client = Client()
        User = get_user_model()
        User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        return self.client


class WsgiTestCase(TestCase):
    def test_wsgi(self):
        from .wsgi import application

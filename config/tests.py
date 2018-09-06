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
        me = get_user_model().objects.all()[0]
        obj.me = me
        obj.frank = Player.objects.create(nick="Frank", owner=me)
        obj.alex = Player.objects.create(nick="Alexandra", owner=me)
        obj.sebi = Player.objects.create(nick="Sebastiano", owner=me)
        obj.uenal = Player.objects.create(nick="Ünal", owner=me)

        obj.devils = Team.objects.create(teamname="Devils", owner=me)
        obj.devils.players.add(obj.frank)
        obj.devils.players.add(obj.sebi)

        obj.dimension = Team.objects.create(teamname="Dimension", owner=me)
        obj.dimension.players.add(obj.frank)
        obj.dimension.players.add(obj.alex)

        obj.nameless_team = Team.objects.create(owner=me)
        obj.nameless_team.players.add(obj.frank)
        obj.nameless_team.players.add(obj.alex)

        obj.empty_team = Team.objects.create(teamname="Empty", owner=me)

        obj.single_team = Team.objects.get(teamname="Frank", owner=me)

        obj.match1 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank", owner=me),
            secondteam=Team.objects.get(teamname="Alexandra", owner=me),
            firstteam_goals=10,
            secondteam_goals=5,
            owner=me,
        )
        obj.match2 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank", owner=me),
            secondteam=Team.objects.get(teamname="Alexandra", owner=me),
            firstteam_goals=5,
            secondteam_goals=10,
            owner=me,
        )

        obj.single_name = Team.objects.create(teamname="SingleName", owner=me)
        obj.single_name.players.add(obj.frank)

        Match.objects.create(
            firstteam=obj.devils,
            secondteam=obj.dimension,
            firstteam_goals=5,
            secondteam_goals=5,
            owner=me,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=5,
            secondteam_goals=5,
            owner=me,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=5,
            secondteam_goals=6,
            owner=me,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=6,
            secondteam_goals=5,
            owner=me,
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

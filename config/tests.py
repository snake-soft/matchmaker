""" tests for config module """
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from player.models import Player
from team.models import Team
from match.models import Match


class TestBase:
    """ Default test initialization for db etc. """

    def __init__(self):
        self.db_ = lambda: None  # _ is for pylint
        self.client = self.create_user_and_login()
        self.create_sample_db()

    def create_sample_db(self):
        """ create sample database entries """
        obj = self.db_
        obj.me_ = get_user_model().objects.all()[0]
        obj.frank = Player.objects.create(nick="Frank", owner=obj.me_)
        obj.alex = Player.objects.create(nick="Alexandra", owner=obj.me_)
        obj.sebi = Player.objects.create(nick="Sebastiano", owner=obj.me_)
        obj.uenal = Player.objects.create(nick="Ünal", owner=obj.me_)

        obj.devils = Team.objects.create(teamname="Devils", owner=obj.me_)
        obj.devils.players.add(obj.frank)
        obj.devils.players.add(obj.sebi)

        obj.dimension = Team.objects.create(
            teamname="Dimension", owner=obj.me_)
        obj.dimension.players.add(obj.frank)
        obj.dimension.players.add(obj.alex)

        obj.nameless_team = Team.objects.create(owner=obj.me_)
        obj.nameless_team.players.add(obj.frank)
        obj.nameless_team.players.add(obj.alex)

        obj.empty_team = Team.objects.create(teamname="Empty", owner=obj.me_)

        obj.single_team = Team.objects.get(teamname="Frank", owner=obj.me_)

        obj.match1 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank", owner=obj.me_),
            secondteam=Team.objects.get(teamname="Alexandra", owner=obj.me_),
            firstteam_goals=10,
            secondteam_goals=5,
            owner=obj.me_,
        )
        obj.match2 = Match.objects.create(
            firstteam=Team.objects.get(teamname="Frank", owner=obj.me_),
            secondteam=Team.objects.get(teamname="Alexandra", owner=obj.me_),
            firstteam_goals=5,
            secondteam_goals=10,
            owner=obj.me_,
        )

        obj.single_name = Team.objects.create(
            teamname="SingleName", owner=obj.me_)
        obj.single_name.players.add(obj.frank)

        Match.objects.create(
            firstteam=obj.devils,
            secondteam=obj.dimension,
            firstteam_goals=5,
            secondteam_goals=5,
            owner=obj.me_,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=5,
            secondteam_goals=5,
            owner=obj.me_,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=5,
            secondteam_goals=6,
            owner=obj.me_,
        )
        Match.objects.create(
            firstteam=obj.dimension,
            secondteam=obj.devils,
            firstteam_goals=6,
            secondteam_goals=5,
            owner=obj.me_,
        )

    def create_user_and_login(self):
        """ create user and log this user in """
        self.client = Client()
        user = get_user_model()
        user.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        return self.client


class WsgiTestCase(TestCase):
    """ tests for wsgi server """

    def test_wsgi(self):
        """ run """
        from .wsgi import application
        _ = application
        _ = self

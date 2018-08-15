''' Only for viewing stats '''
from django.db import models
from match.models import Match
from player.models import Player
from team.models import Team


class PlayerStats(Player):
    def __init__(self, id):
        self.id = id

    def games_played(self):
        import pdb; pdb.set_trace()
        return "1"


class TeamStats:
    def __init__(self, id):
        self.id = id


class MatchStats:
    def __init__(self, id):
        self.id = id

pstats = PlayerStats(1)
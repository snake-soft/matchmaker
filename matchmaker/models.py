""" matchmaker model (no database) """
from itertools import combinations as comb
from math import ceil
from team.models import Team
from match.models import Match


class ConstellationFactory:
    """ Factory that calculates constellations from players and count """

    def __init__(self, players, count):
        self.players = players
        self.count = count
        self.get_constellations()

    @property
    def teamsize(self):
        """ returns (sizeoffirstteam, sizeofsecondteam) """
        return ceil(self.count / 2), self.count - ceil(self.count / 2)

    def get_constellations(self):
        """ returns list of possible constellations
        sorted by strength difference
        """
        def team_calculator(players, t1_size, t2_size):
            combi1 = tuple(comb(players, t1_size))
            combi2 = tuple(comb(players, t2_size))
            used, ret = [], []

            for team1 in combi1:
                if team1 not in used:
                    for team2 in combi2:
                        if team2 not in used \
                                and not any([x for x in team2 if x in team1]):
                            ret.append(Constellation(team1, team2))
                            used.append(team1)
            return ret

        ret = team_calculator(self.players, self.teamsize[0], self.teamsize[1])
        return sorted(ret, key=lambda x: x.difference)


class Constellation:
    """ team1 vs team2 -> constellation """

    def __init__(self, players_t1, players_t2):
        self.team1 = self.get_constellation_team(players_t1)
        self.team2 = self.get_constellation_team(players_t2)

    @property
    def difference(self):
        """ difference of the team strength """
        ret = self.team1.strength - self.team2.strength
        return ret if ret >= 0 else ret * -1

    @property
    def chance(self):
        """ returns t1chance, t2chance """
        elo_t1 = Elo(self.team1.strength)
        expected = elo_t1.expected(self.team2.strength)
        return int(expected * 100 + 0.5), int((1 - expected) * 100 + 0.5)

    @staticmethod
    def get_constellation_team(players):
        """ returns single constellation """
        return ConstellationTeam(players)

    @property
    def previous_matches(self):
        """ previous matches of this constellation """
        return Match.previous_matches(self.team1.team, self.team2.team)


class ConstellationTeam:
    """ single team """

    def __init__(self, players):
        self.players = players
        self.team = Team.players_have_team(self.players)

    @property
    def player_ids(self):
        """ returns list of player ids """
        return [x.id for x in self.players]

    @property
    def strength(self):
        ''' needs dry fix - is also in Team but not all are existing '''
        return int(sum([x.player_rating() for x in self.players])
                   / len(self.players) + 0.5)

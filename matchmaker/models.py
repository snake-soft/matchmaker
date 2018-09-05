from team.models import Team
from math import ceil
from itertools import combinations as comb


class ConstellationFactory:
    def __init__(self, players, count):
        self.players = players
        self.count = count
        self.get_constellations()

    @property
    def teamsize(self):
        """ returns (sizeoffirstteam, sizeofsecondteam) """
        return ceil(self.count / 2), self.count - ceil(self.count / 2)

    def get_constellations(self):
        def team_calculator(players, t1_size, t2_size):
            combi1 = tuple(comb(players, t1_size))
            combi2 = tuple(comb(players, t2_size))
            used, ret = [], []

            for t1 in combi1:
                if t1 not in used:
                    for t2 in combi2:
                        if t2 not in used \
                                and not any([x for x in t2 if x in t1]):
                            ret.append(Constellation(t1, t2))
                            used.append(t1)
            return ret

        ret = team_calculator(self.players, self.teamsize[0], self.teamsize[1])
        return sorted(ret, key=lambda x: x.difference)


class Constellation:
    def __init__(self, players_t1, players_t2):
        self.team1 = ConstellationTeam(players_t1)
        self.team2 = ConstellationTeam(players_t2)

    @property
    def difference(self):
        # could be better, recognizing unequal team sizes
        t1_strength = self.team1.strength
        t2_strength = self.team2.strength
        ret = t1_strength - t2_strength
        return ret if ret >= 0 else ret * -1


class ConstellationTeam:
    def __init__(self, players):
        self.players = players
        self.team = Team.players_have_team(self.players)

    @property
    def player_ids(self):
        return [x.id for x in self.players]

    @property
    def strength(self):
        ''' needs dry fix - is also in Team but not all are existing '''
        return int(sum([x.player_rating() for x in self.players])
                   / len(self.players) + 0.5)

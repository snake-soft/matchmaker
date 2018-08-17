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
        ret = []
        if self.teamsize[0] - self.teamsize[1] is 0:
            combinations = tuple(comb(self.players, self.teamsize[0]))
            for t1 in combinations:
                non_t1 = tuple(x for x in self.players if x not in t1)
                import pdb; pdb.set_trace()  # <---------
                ret.append(Constellation(t1, non_t1))
            #import pdb; pdb.set_trace()  # <---------
        else:
            for t1 in tuple(comb(self.players, self.teamsize[0])):
                non_t1 = [x for x in self.players if x not in t1]
                for t2 in tuple(comb(non_t1, self.teamsize[1])):
                    ret.append(Constellation(t1, t2,))
        return sorted(ret, key=lambda x: x.difference)


class Constellation:
    def __init__(self, players_t1, players_t2):
        self.team1 = ConstellationTeam(players_t1)
        self.team2 = ConstellationTeam(players_t2)

    @property
    def player_count(self):  # unused
        """ 0->Teams are equal; <0: Team2 is bigger; >0-> Team1 is bigger """
        return len(self.team1.players) - len(self.team2.players)

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
    def strength(self):
        ''' needs dry fix - is also in Team but not all are existing '''
        return int(sum([x.player_rating() for x in self.players])
                   / len(self.players) + 0.5)

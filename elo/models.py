

class Elo:
    """ Class for managing a Elo-like rating System
    to evaluate the skills of a Player
    Differences to the Original Elo-System are:
    - Goal difference is considered
    - K value calculation simplified
    """

    def __init__(self, current_elo=1000):
        self.elo = current_elo

    def new_result(self, enemy_elo, goal_diff):
        """ returns new result from existing elo and goal difference """
        exp = self.expected(enemy_elo)
        return self.new_elo(exp, goal_diff)

    def expected(self, enemy_elo):
        """ returns the excepted match result """
        return Elo._expected(self.elo, enemy_elo)

    def new_elo(self, exp, goal_diff):
        """ returns new elo from expected and goal difference """
        return Elo._new_elo(self.elo, exp, goal_diff)

    @staticmethod
    def mapper(value, range_from, range_to, limit_to=True):
        """ maps value from range(min_from-max_from) to (min_to-max_to)
        :param value: value to map
        :param range_from: (min_from, max_from)
        :param range_to: (min_to, max_to)
        :param limit_to: False if value can be out of range
        """
        min_from, max_from = range_from
        min_to, max_to = range_to
        ret = min_to + (max_to - min_to) * ((value - min_from) /
                                            (max_from - min_from))
        if limit_to:
            if ret < min(min_to, max_to):
                ret = min(min_to, max_to)
            elif ret > max(max_to, min_to):
                ret = max(max_to, min_to)
        return ret

    @staticmethod
    def _expected(player_a, player_b):
        """ Calculate expected score of A in a match against B
        :param player_a: Elo rating for player A
        :param player_b: Elo rating for player B
        """
        if player_b - player_a < -400:
            dif = -400
        if player_b - player_a > 400:
            dif = 400
        else:
            dif = player_b - player_a
        return 1 / (1 + 10 ** ((dif) / 400))

    @staticmethod
    def _new_elo(old, exp, goal_diff):
        """ Calculate the new Elo rating for a player
        :param old: The previous Elo rating
        :param exp: The expected score for this match
        :param goal_diff: Goal difference
        """
        # Original score: win 1, draw 0.5, lose 0
        score = 0.5 + goal_diff / 10

        # Original k: default->20, elo>2400->10, less30matches->40, <18yo->40
        # Here k is mapped to the range of possible k-values (40-10)
        k = Elo.mapper(old, (0, 2400), (40, 10))
        new_elo = old + k * (score - exp)
        return new_elo if new_elo >= 0 else 0

    def __str__(self):
        ''' I love chess but against hard enemys my brain hurts '''
        return str(int(self.elo + 0.5))

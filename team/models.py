from django.db import models

from match.models import Match


class Team(models.Model):
    """ Teams are Season-based
    -> every season there are new values
    -> values are calculated from the matches
    """
    teamname = models.CharField(
        max_length=50, verbose_name="Teamname",
        blank=True
        )
    players = models.ManyToManyField('player.Player')

    def new_result(self, own_goals, foreign_goals):
        if own_goals == foreign_goals:
            self.tscore += 1
        elif own_goals > foreign_goals:
            self.tscore += 2
        self.save()

    @property
    def team_score(self):
        ''' calculate based on matches '''
        results = self.get_win_draw_lose()
        return len(results[0]) * 2 + len(results[1]) * 1

    @property
    def team_rating(self):
        """ Calculates the team strength out of the Player Elo """
        return sum([x.player_rating() for x in self.players.all()])

    def get_team_name_or_members(self):
        if self.teamname:
            return self.teamname
        else:
            return ', '.join([x.nick for x in self.players.all()])

    def get_win_draw_lose(self):
        win, draw, lose = [], [], []
        matches = [x for x in Match.objects.filter(firstteam_id=self.pk)]
        for match in matches:
            result = match.firstteam_goals - match.secondteam_goals
            if result > 0:
                win.append(match)
            elif result is 0:
                draw.append(match)
            elif result < 0:
                lose.append(match)

        matches = [x for x in Match.objects.filter(secondteam_id=self.pk)]
        for match in matches:
            result = match.secondteam_goals - match.firstteam_goals
            if result > 0:
                win.append(match)
            elif result is 0:
                draw.append(match)
            elif result < 0:
                lose.append(match)

        return (win, draw, lose)

    def __str__(self):
        return str(
            "%s (TeamScore: %s; TeamRating: %s Members: %s)" % (
                self.get_team_name_or_members(),
                int(self.team_score + 0.5),
                int(self.team_rating + 0.5),
                ", ".join([x.nick for x in self.players.all()])
                )
            )

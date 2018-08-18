from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

from match.models import Match


# CHECK IF AN IDENTICAL TEAM EXISTS
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

    @property
    def name(self):
        return self.get_team_name_or_members()

    @property
    def team_score(self):
        ''' calculate based on matches '''
        results = self.get_win_draw_lose()
        return len(results[0]) * 2 + len(results[1]) * 1

    @property
    def team_rating(self):
        """ Calculates the team strength out of the Player Elo """
        return sum([x.player_rating() for x in self.players.all()]) / len(self.players.all())

    @property
    def team_rating_as_int(self):
        return int(self.team_rating + 0.5)

    def get_team_name_or_members(self):
        if self.teamname:
            return self.teamname
        else:
            return '<%s>' % (', '.join([x.nick for x in self.players.all()]))

    def get_win_draw_lose(self, start_date=False, end_date=False):
        win, draw, lose = [], [], []
        start_date = start_date if start_date else date(2000, 1, 1)
        end_date = end_date if end_date else date(3000, 1, 1)
        matches = Match.objects.filter(
            firstteam_id=self.pk,
            date_time__range=(start_date, end_date)
            )
        for match in matches:
            result = match.firstteam_goals - match.secondteam_goals
            if result > 0:
                win.append(match)
            elif result is 0:
                draw.append(match)
            elif result < 0:
                lose.append(match)

        matches = Match.objects.filter(
            secondteam_id=self.pk,
            date_time__range=(start_date, end_date)
            )
        for match in matches:
            result = match.secondteam_goals - match.firstteam_goals
            if result > 0:
                win.append(match)
            elif result is 0:
                draw.append(match)
            elif result < 0:
                lose.append(match)
        return win, draw, lose

    @classmethod
    def players_have_team(cls, player_obj_lst):
        def list_compare(old, new):
            """ return{'rem':[miss in new], 'add':[miss in old]} """
            return {
                'rem': [x for x in old if x not in new],
                'add': [x for x in new if x not in old]
                }
        for team in cls.objects.all():
            compared = list_compare(player_obj_lst, team.players.all())
            if len(compared['rem']) is 0 and len(compared['add']) is 0:
                return team
        return None

    def save(self):
        super().save()
        import pdb; pdb.set_trace()  # <---------
        #=======================================================================
        # if __class__.players_have_team(self.players):
        #     raise ValidationError(
        #         "This team already exists" % (
        #             str(self.firstteam.id) + "",
        #             ),
        #         params={'value': self.firstteam.id},
        #         )
        # else:
        #     super().save()
        #=======================================================================

    def __str__(self):
        return str(
            "%s (TeamScore: %s; TeamRating: %s Members: %s)" % (
                self.get_team_name_or_members(),
                int(self.team_score + 0.5),
                int(self.team_rating + 0.5),
                ", ".join([x.nick for x in self.players.all()])
                )
            )

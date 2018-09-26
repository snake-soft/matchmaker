from django.db import models
from match.models import Match
from datetime import date, datetime, timedelta
from django.utils.decorators import classproperty


class PlayerTeamBase(models.Model):
    name = models.CharField(max_length=50, verbose_name="Playername", blank=True)
    frm = datetime(2000, 1, 1).date()
    to_ = datetime(3000, 1, 1).date()
    communities = None   # FROM PLAYERS!!!
    strength = None
    get_players = None
    new_result = None
    active_community = None

    #===========================================================================
    # @property
    # def class_(self):
    #     return self.__class__.__name__.lower()
    #===========================================================================

    @classmethod
    def set_from_to(cls, frm=None, to_=None):
        def to_date(date_x):
            """ date_x may be date, datetime or string object
            returns date object
            """
            return {
                datetime: lambda: date_x.date,
                date: lambda: date_x,
                str: lambda: datetime.strptime(date_x, '%Y-%m-%d').date(),
            }.get(type(date_x))()
        if frm:
            cls.frm = to_date(frm)
        if to_:
            cls.to_ = to_date(to_) + timedelta(days=1)

    @property
    def score(self):
        return sum([match.pov().goal_difference for match in self.matches])

    @property
    def strength_as_int(self):
        return int(self.strength + 0.5)

    @property
    def matches(self):
        return sorted(Match.objects.filter(
            models.Q(firstteam=self) | models.Q(secondteam=self),
            date_time__range=(self.frm, self.to_), key=id
        ))

    @property
    def matches_pov(self):
        return [match.pov for match in self.matches]

    @property
    def get_win_draw_lose(self):
        ret = {'win': [], 'draw': [], 'lose': []}
        for match in self.matches_pov:
            if match.firstteam_goals > match.secondteam_goals:
                ret['win'].append(match)
            elif match.firstteam_goals < match.secondteam_goals:
                ret['lose'].append(match)
            else:
                ret['draw'].append(match)
        return ret

    class Meta:
        abstract = True



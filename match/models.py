""" Match model """
from datetime import date, datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Match(models.Model):
    """ Match model
    workaround: frm and to_ are the last setted datefilters
    I dont want to have requests inside the model
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    firstteam = models.ForeignKey(
        'team.Team',
        related_name='Team1',
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Team 1",
    )

    secondteam = models.ForeignKey(
        'team.Team',
        related_name='Team2',
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Team 2",
    )

    firstteam_goals = models.PositiveSmallIntegerField(
        verbose_name="T1 goals",
        default=0
    )

    secondteam_goals = models.PositiveSmallIntegerField(
        verbose_name="T2 goals",
        default=0
    )

    date_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name="Finish-Date",
    )

    frm = datetime(2000, 1, 1).date()
    to_ = datetime(3000, 1, 1).date()

    @classmethod
    def set_from_to(cls, frm, to_):
        """ sets new date filter """
        def to_date(date_x):
            """ date_x may be date, datetime or string object
            returns date object
            """
            return {
                datetime: lambda: date_x.date,
                date: lambda: date_x,
                str: lambda: datetime.strptime(date_x, '%Y-%m-%d').date(),
            }.get(type(date_x))()

        cls.frm = to_date(frm)
        cls.to_ = to_date(to_) + timedelta(days=1)

    @property
    def goal_difference(self):
        """ positiv=win_firstteam, negativ=win_secondteam """
        return self.firstteam_goals - self.secondteam_goals

    @property
    def rematches(self):
        """ returns list of matches with same teams """
        ret = self.previous_matches(self.firstteam, self.secondteam)
        return [x for x in sorted(ret, key=lambda x: x.pk)
                if x.pk is not self.pk]

    @property
    def rematches_erlier_later(self):
        """ returns rematches (earlier, later) """
        earlier, later = [], []
        for match in self.rematches:
            if match.date_time < self.date_time:
                earlier.append(match)
            else:
                later.append(match)
        return earlier, later

    @classmethod
    def previous_matches(cls, firstteam, secondteam):
        """ calculates previous matches by firstteam, secondteam """
        ret = []
        ret += cls.objects.filter(firstteam=firstteam, secondteam=secondteam,
                                  date_time__range=(cls.frm, cls.to_))
        ret += cls.objects.filter(firstteam=secondteam, secondteam=firstteam,
                                  date_time__range=(cls.frm, cls.to_))
        return sorted(ret, key=lambda x: x.pk)

    def new_result(self):
        """ sets new result to players """
        for player in self.firstteam.players.all():
            player.new_result(
                self.firstteam_goals - self.secondteam_goals,
                self.secondteam
            )

        for player in self.secondteam.players.all():
            player.new_result(
                self.secondteam_goals - self.firstteam_goals,
                self.secondteam
            )

    def save(self, *args, **kwargs):  # pylint: disable=W0221
        if self.firstteam.pk is self.secondteam.pk:
            raise ValidationError(
                "%s can't play against itself" % (
                    str(self.firstteam.pk) + "",
                ),
                params={'value': self.firstteam.pk},
            )
        else:
            self.new_result()
            super().save(*args, **kwargs)

    def __str__(self):
        return str("ID%s: %s vs. %s (%s:%s)" % (
            self.id,
            self.firstteam.get_team_name_or_members(),
            self.secondteam.get_team_name_or_members(),
            self.firstteam_goals,
            self.secondteam_goals,
        ))

    class Meta:
        verbose_name_plural = "Matches"

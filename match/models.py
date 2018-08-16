from django.db import models
from django.core.exceptions import ValidationError


class Match(models.Model):
    from team.models import Team
    firstteam = models.ForeignKey(
        Team,
        related_name='Team1',
        on_delete=models.CASCADE,
        default=None,
        verbose_name="Team 1",
        )

    secondteam = models.ForeignKey(
        Team,
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

    def new_result(self):
        self.firstteam.new_result(self.firstteam_goals, self.secondteam_goals)
        for x in self.firstteam.players.all():
            x.new_result(
                self.firstteam_goals - self.secondteam_goals,
                self.secondteam
                )

        self.secondteam.new_result(self.secondteam_goals, self.firstteam_goals)
        for x in self.secondteam.players.all():
            x.new_result(
                self.secondteam_goals - self.firstteam_goals,
                self.secondteam
                )

    def save(self):
        if self.firstteam.id is self.secondteam.id:
            raise ValidationError(
                "%s can't play against itself" % (
                    str(self.firstteam.id) + "",
                    ),
                params={'value': self.firstteam.id},
                )
        else:
            self.new_result()
            super().save()

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


class stats:
    


#===============================================================================
# def result_pre_save(**kwargs):
#     if kwargs['instance'].firstteam.id is kwargs['instance'].secondteam.id:
#         raise ValidationError(
#             "%s can't play against itself" % (
#                 str(kwargs['instance'].firstteam.id) + "",
#                 ),
#             params={'value': kwargs['instance'].firstteam.id},
#             )
#     else:
#         kwargs['instance'].new_result()
# 
# 
# models.signals.pre_save.connect(result_pre_save, sender=Match)
#===============================================================================

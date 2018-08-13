from django.db import models
from team.models import Team


class Match(models.Model):
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

    date_time = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name="Finish-Date",
        )

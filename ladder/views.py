from django.shortcuts import render
from django.views.generic import ListView

from team.models import Team
from player.models import Player

class OverviewTeamPlayer(ListView):
    model = Player
    #template_name = "ladder/overview.html"
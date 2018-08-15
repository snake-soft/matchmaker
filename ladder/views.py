from django.shortcuts import render
from django.views.generic import ListView

from team.models import Team
from player.models import Player


class OverviewTeamPlayer(ListView):
    model = Player
    context_object_name = 'object_list'
    queryset = Player.objects.all()
    # template_name = "ladder/overview.html"

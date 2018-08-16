from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Player


class PlayerList(ListView):
    model = Player
    context_object_name = 'object_list'
    queryset = Player.objects.all()
    # template_name = "ladder/overview.html"


class PlayerDetails(DetailView):
    model = Player

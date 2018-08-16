from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Player


class PlayerList(ListView):
    model = Player


class PlayerDetails(DetailView):
    model = Player

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Team


class TeamList(ListView):
    model = Team


class TeamDetails(DetailView):
    model = Team

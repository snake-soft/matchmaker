from django.shortcuts import render
from django.views.generic import CreateView
from match.models import Match


class ControlView(CreateView):
    model = Match
    fields = ['firstteam', 'secondteam', 'firstteam_goals', 'secondteam_goals']
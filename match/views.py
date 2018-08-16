from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Match


class MatchList(ListView):
    model = Match


class MatchDetails(DetailView):
    model = Match

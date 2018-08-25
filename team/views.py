from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django import forms

from .models import Team
from .forms import TeamCreateForm


class TeamList(ListView):
    model = Team


class TeamListRealtime(ListView):
    model = Team
    template_name = 'team/team_list_realtime.html'
    '''
    Faktoren temporär zu ändern:
    Player Elo
    Team Score
    Team Win Draw Lose
    '''


class TeamDetails(DetailView):
    model = Team


class TeamCreate(CreateView):
    model = Team
    form_class = TeamCreateForm

    def get_initial(self):
        self.success_url = reverse('team-list')
        # self.success_url = self.request.path
        initial = super(CreateView, self).get_initial()
        initial = initial.copy()

        if 'players' in self.request.GET:
            initial['players'] = [int(x) for x in self.request.GET['players'].split(',')]
        return initial

    def post(self, request):
        return super().post(request)


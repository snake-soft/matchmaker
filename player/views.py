""" views for player """
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from team.models import Team
from .models import Player


class PlayerList(LoginRequiredMixin, ListView):\
        # pylint: disable=too-many-ancestors
    """ view list of players """
    model = Player

    def get_queryset(self):
        """ get only own players """
        return Player.objects.filter(owner=self.request.user)


class PlayerDetails(LoginRequiredMixin, DetailView):\
        # pylint: disable=too-many-ancestors
    """ view details of single player """
    model = Player

    def get_queryset(self):
        """ get only own players """
        return Player.objects.filter(owner=self.request.user)


class PlayerCreate(LoginRequiredMixin, CreateView):\
        # pylint: disable=too-many-ancestors
    """ form for creating new player """
    model = Player
    fields = ['nick']

    def form_valid(self, form):
        name = form.cleaned_data['nick']
        owner = self.request.user
        form.instance.owner = owner
        player_exists = Player.objects.filter(nick__iexact=name, owner=owner)
        team_exists = Team.objects.filter(teamname__iexact=name, owner=owner)
        if player_exists or team_exists:
            form.errors['error'] = name + ' already exists'
            return super().form_invalid(form)
        return super().form_valid(form)

    def get_initial(self):
        self.success_url = reverse('ladder')  # self.request.path

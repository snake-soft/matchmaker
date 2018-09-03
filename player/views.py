from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from .models import Player
from team.models import Team


class PlayerList(LoginRequiredMixin, ListView):
    model = Player

    def get_queryset(self):
        return Player.objects.filter(owner=self.request.user)


class PlayerDetails(LoginRequiredMixin, DetailView):
    model = Player

    def get_queryset(self):
        return Player.objects.filter(owner=self.request.user)


class PlayerCreate(LoginRequiredMixin, CreateView):
    model = Player
    fields = ['nick']

    def form_valid(self, form, *args, **kwargs):
        name = form.cleaned_data['nick']
        owner = self.request.user
        form.instance.owner = owner
        player_exists = Player.objects.filter(nick__iexact=name, owner=owner)
        team_exists = Team.objects.filter(teamname__iexact=name, owner=owner)
        if len(player_exists) or len(team_exists):
            form.errors['error'] = name + ' already exists'
            return super().form_invalid(form, *args, **kwargs)
        return super().form_valid(form, *args, **kwargs)

    def get_initial(self):
        self.success_url = reverse('ladder')  # self.request.path

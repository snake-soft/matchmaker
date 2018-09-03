from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

from .models import Player


class PlayerList(LoginRequiredMixin, ListView):
    model = Player


class PlayerDetails(LoginRequiredMixin, DetailView):
    model = Player


class PlayerCreate(LoginRequiredMixin, CreateView):
    model = Player
    fields = ['nick']

    def get_initial(self):
        self.success_url = reverse('player-list')  # self.request.path

    def post(self, request):
        return super().post(request)

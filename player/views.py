from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponseRedirect

from .models import Player


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
        owner = self.request.user
        form.instance.owner = owner
        return super().form_valid(form, *args, **kwargs)

    def get_initial(self):
        self.success_url = reverse('player-list')  # self.request.path

    #===========================================================================
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['owner'] = self.request.user
    #     return kwargs
    #===========================================================================
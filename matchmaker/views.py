from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .forms import MatchmakerForm
from .models import ConstellationFactory
from player.models import Player


class MatchmakerView(LoginRequiredMixin, View):

    def get(self, request):
        self.context = {}
        if 'players' and 'count' in request.GET:
            request.session['last_players'] = request.GET.getlist('players')
            request.session['last_count'] = request.GET.get('count')
            players = [Player.objects.get(pk=x)
                       for x in request.GET.getlist('players')]
            self.context['constellations'] = ConstellationFactory(
                players, int(request.GET.get('count'))
                ).get_constellations()
            x = self.context['constellations']

        self.context["matchmaker_form"] = MatchmakerForm(request)
        return render(
            request,
            template_name="matchmaker/matchmaker_form.html",
            context=self.context,
            )

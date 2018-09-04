from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .forms import MatchmakerForm
from .models import ConstellationFactory
from player.models import Player


class MatchmakerView(LoginRequiredMixin, View):
    def get(self, request):
        self.context = {}
        request.session['last_players'] = request.GET.getlist('players')
        request.session['last_count'] = request.GET.get('count')
        form = MatchmakerForm(request)
        if 'players' and 'count' in request.GET:
            players = [Player.objects.get(pk=x, owner=request.user)
                       for x in request.GET.getlist('players')]
            self.context['constellations'] = ConstellationFactory(
                players, int(request.GET.get('count'))
            ).get_constellations()
            x = self.context['constellations']
            if len(request.GET.getlist('players')) \
                    < int(request.GET.get('count')):
                form.errors['error'] = 'Choose more players !'
        self.context["matchmaker_form"] = form
        return render(
            request,
            template_name="matchmaker/matchmaker_form.html",
            context=self.context,
        )

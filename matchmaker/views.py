from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .forms import MatchmakerForm
from .models import ConstellationFactory
from player.models import Player


class MatchmakerView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        request.session['last_players'] = request.GET.getlist('players')
        request.session['last_count'] = request.GET.get('count')
        initial_count = int(request.session['last_count']) \
            if request.session['last_count'] else 2
        initial_players = request.session['last_players'] \
            if len(request.session['last_players']) else ''
        form = MatchmakerForm(request, initial={
            'count': initial_count,
            'players': initial_players,
            })
        if 'players' and 'count' in request.GET:
            players = [Player.objects.get(pk=x, owner=request.user)
                       for x in request.GET.getlist('players')]
            context['constellations'] = ConstellationFactory(
                players, int(request.GET.get('count'))
            ).get_constellations()
            if len(request.GET.getlist('players')) \
                    < int(request.GET.get('count')):
                form.errors['error'] = 'Choose more players !'
        context["matchmaker_form"] = form
        return render(
            request,
            template_name="matchmaker/matchmaker_form.html",
            context=context,
        )

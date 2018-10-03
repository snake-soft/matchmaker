""" views for balancer module """
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from player.models import Player
from team.forms import TeamCreateForm
from match.models import Match
from balancer.forms import BalancerForm
from balancer.models import ConstellationFactory


class MatchmakerView(LoginRequiredMixin, View):
    """ balancer himself """

    def get(self, request):
        """ get method of balancer """
        Match.set_from_to(
            self.request.session['from'], self.request.session['to'])
        context = {}

        if 'players' in request.GET:
            request.session['last_players'] = request.GET.getlist('players')
        if 'count' in request.GET:
            request.session['last_count'] = request.GET.get('count')

        initial_count = int(request.session['last_count']) \
            if 'last_count' in request.session \
            and request.session['last_count'] \
            else 2
        initial_players = request.session['last_players'] \
            if 'last_players' in request.session \
            and request.session['last_players'] \
            else ''

        form = BalancerForm(request, initial={
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
            template_name="balancer/matchmaker_form.html",
            context=context,
        )

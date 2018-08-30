from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django import forms

from .models import Team
from player.models import Player, Elo
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
    def get_context_data(self, *args, **kwargs):
        context = super(__class__, self).get_context_data(*args, **kwargs)
        firstteam = Team.objects.get(pk=int(self.request.GET['firstteam']))
        secondteam = Team.objects.get(pk=int(self.request.GET['secondteam']))
        context['team_realtime'] = [
            self.TeamRealtimeValues(
                firstteam,
                secondteam,
                int(self.request.GET['firstteam_goals']),
                int(self.request.GET['secondteam_goals']),
                ),
            self.TeamRealtimeValues(
                secondteam,
                firstteam,
                int(self.request.GET['secondteam_goals']),
                int(self.request.GET['firstteam_goals']),
                )
            ]
        context['player_realtime'] = []
        for player in firstteam.players.all():
            context['player_realtime'].append(self.PlayerRealtimeValues(
                player,
                secondteam,
                int(self.request.GET['firstteam_goals']) - int(self.request.GET['secondteam_goals'])
                )
            )
        return context

    class TeamRealtimeValues:
        def __init__(self, own_team, enemy, own_goals, enemy_goals):
            self.own_team = own_team
            self.enemy = enemy
            self.own_goals = own_goals
            self.enemy_goals = enemy_goals

        def team_score(self):
            score = self.own_team.team_score
            if self.own_goals > self.enemy_goals:
                score += 2
            elif self.own_goals == self.enemy_goals:
                score += 1
            return score

        def team_score_diff(self):
            return self.team_score() - self.own_team.team_score

        def team_wdl(self):
            wdl = self.own_team.get_win_draw_lose()
            if self.own_goals > self.enemy_goals:
                wdl[0].append("Realtime")
            elif self.own_goals == self.enemy_goals:
                wdl[1].append("Realtime")
            elif self.own_goals < self.enemy_goals:
                wdl[2].append("Realtime")
            return wdl

        def team_wdl_diff(self):
            wdl = self.team_wdl()
            wdl_orig = self.own_team.get_win_draw_lose()
            return [
                len(wdl[0]) - len(wdl_orig[0]),
                len(wdl[1]) - len(wdl_orig[1]),
                len(wdl[2]) - len(wdl_orig[2])
                ]

        def close_wl(self):
            close_wl = self.own_team.close_win_lose
            if self.own_goals - self.enemy_goals == 1:
                close_wl[0].append("Realtime")
            elif self.own_goals - self.enemy_goals == -1:
                close_wl[1].append("Realtime")
            return close_wl

        def close_wl_diff(self):
            close_wl = self.close_wl()
            close_wl_orig = self.own_team.close_win_lose
            return [
                len(close_wl[0]) - len(close_wl_orig[0]),
                len(close_wl[1]) - len(close_wl_orig[1])
                ]

        def strength(self):
            return self.own_team.team_rating()

        def strength_diff(self):
            return self.own_team.team_rating()

    class PlayerRealtimeValues:
        def __init__(self, player, enemy_team, goal_diff):
            self.player = player
            self.enemy_team = enemy_team
            self.goal_diff = goal_diff
            self.elo = self._new_elo() + 0.5
            self.elo_as_int = int(self.elo + 0.5)

        def _new_elo(self):
            elo = Elo(self.player.rating)
            return elo.new_result(
                self.enemy_team.team_rating,
                self.goal_diff
                )

        def elo_diff(self):
            return int((self.player.rating - self.elo) + 0.5)


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


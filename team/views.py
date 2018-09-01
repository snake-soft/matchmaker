from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

from .models import Team
from player.models import Elo
from .forms import TeamCreateForm


class TeamList(ListView):
    model = Team


class TeamListRealtime(ListView):
    model = Team
    template_name = 'team/team_list_realtime.html'

    def get_context_data(self, *args, **kwargs):
        context = super(__class__, self).get_context_data(*args, **kwargs)
        if 'firstteam' in self.request.GET and self.request.GET['firstteam']:
            context = self.init_teams(context)
        return context

    def init_teams(self, context):
        self.request.session['last_firstteam'] = int(
            self.request.GET['firstteam']
            )
        self.request.session['last_secondteam'] = int(
            self.request.GET['secondteam']
            )
        firstteam = Team.objects.get(pk=int(self.request.GET['firstteam']))
        secondteam = Team.objects.get(pk=int(self.request.GET['secondteam']))

        context['player_realtime'] = {}
        for player in firstteam.players.all():  # BEFORE TEAM REALTIME!
            obj = self.PlayerRealtimeValues(
                player,
                secondteam,
                int(self.request.GET['firstteam_goals'])
                - int(self.request.GET['secondteam_goals'])
            )
            context['player_realtime'][obj.pk] = obj
        for player in secondteam.players.all():  # BEFORE TEAM REALTIME!
            obj = self.PlayerRealtimeValues(
                player,
                firstteam,
                int(self.request.GET['secondteam_goals'])
                - int(self.request.GET['firstteam_goals'])
            )
            context['player_realtime'][obj.pk] = obj

        context['team_realtime'] = {}
        obj = self.TeamRealtimeValues(
            self.request,
            firstteam,
            secondteam,
            int(self.request.GET['firstteam_goals']),
            int(self.request.GET['secondteam_goals']),
            context['player_realtime'],
        )
        context['team_realtime'][obj.pk] = obj
        obj = self.TeamRealtimeValues(
            self.request,
            secondteam,
            firstteam,
            int(self.request.GET['secondteam_goals']),
            int(self.request.GET['firstteam_goals']),
            context['player_realtime'],
        )
        context['team_realtime'][obj.pk] = obj
        return context

    class TeamRealtimeValues:
        def __init__(self, request, own_team, enemy, own_goals, enemy_goals,
                     player_rt):
            self.request = request
            self.own_team = own_team
            self.own_team.set_from_to(
                self.request.session['from'],
                self.request.session['to']
                )
            self.pk = own_team.pk
            self.enemy = enemy
            self.enemy.set_from_to(
                self.request.session['from'],
                self.request.session['to']
                )
            self.own_goals = own_goals
            self.enemy_goals = enemy_goals
            self.player_realtimes = player_rt

        @property
        def team_score(self):
            score = self.own_team.team_score
            if self.own_goals > self.enemy_goals:
                score += 2
            elif self.own_goals == self.enemy_goals:
                score += 1
            return score

        @property
        def team_score_diff(self):
            return self.team_score - self.own_team.team_score

        @property
        def team_wdl(self):
            wdl = self.own_team.get_win_draw_lose()
            if self.own_goals > self.enemy_goals:
                wdl[0].append("Realtime")
            elif self.own_goals == self.enemy_goals:
                wdl[1].append("Realtime")
            elif self.own_goals < self.enemy_goals:
                wdl[2].append("Realtime")
            return wdl

        @property
        def team_wdl_diff(self):
            wdl = self.team_wdl
            wdl_orig = self.own_team.get_win_draw_lose()
            return [
                len(wdl[0]) - len(wdl_orig[0]),
                len(wdl[1]) - len(wdl_orig[1]),
                len(wdl[2]) - len(wdl_orig[2])
            ]

        @property
        def team_win(self):
            return self.team_wdl[0]

        @property
        def team_draw(self):
            return self.team_wdl[1]

        @property
        def team_lose(self):
            return self.team_wdl[2]

        @property
        def team_wdl_factor(self):
            return len(self.team_win) - len(self.team_lose)

        @property
        def team_win_diff(self):
            return self.team_wdl_diff[0]

        @property
        def team_draw_diff(self):
            return self.team_wdl_diff[1]

        @property
        def team_lose_diff(self):
            return self.team_wdl_diff[2]

        @property
        def close_wl(self):
            close_wl = self.own_team.close_win_lose
            if self.own_goals - self.enemy_goals == 1:
                close_wl[0].append("Realtime")
            elif self.own_goals - self.enemy_goals == -1:
                close_wl[1].append("Realtime")
            return close_wl

        @property
        def close_win(self):
            return self.close_wl[0]

        @property
        def close_lose(self):
            return self.close_wl[1]

        @property
        def close_win_diff(self):
            return self.close_wl_diff[0]

        @property
        def close_lose_diff(self):
            return self.close_wl_diff[1]

        @property
        def close_wl_factor(self):
            return len(self.close_win) - len(self.close_lose)

        @property
        def close_wl_diff(self):
            close_wl = self.close_wl
            close_wl_orig = self.own_team.close_win_lose
            return [
                len(close_wl[0]) - len(close_wl_orig[0]),
                len(close_wl[1]) - len(close_wl_orig[1])
            ]

        @property
        def goal_own_foreign(self):
            own, foreign = self.own_team.goal_own_foreign
            own += self.own_goals
            foreign += self.enemy_goals
            return own, foreign

        @property
        def goal_own(self):
            return self.goal_own_foreign[0]

        @property
        def goal_foreign(self):
            return self.goal_own_foreign[1]

        @property
        def goal_factor(self):
            return self.goal_own - self.goal_foreign

        @property
        def strength(self):
            tmp = []
            for player in self.own_team.players.all():
                for player_rt in self.player_realtimes.values():
                    if player.pk == player_rt.player.pk:
                        tmp.append(player_rt.elo)
            return int(sum(tmp) / len(tmp) + 0.5)

        @property
        def strength_diff(self):
            return self.strength - int(self.own_team.team_rating + 0.5)

    class PlayerRealtimeValues:
        def __init__(self, player, enemy_team, goal_diff):
            self.player = player
            self.pk = player.pk
            self.enemy_team = enemy_team
            self.goal_diff = goal_diff
            self.elo = self._new_elo()
            self.elo_as_int = int(self.elo + 0.5)

        def _new_elo(self):
            elo = Elo(self.player.rating)
            return elo.new_result(
                self.enemy_team.team_rating,
                self.goal_diff
            )

        @property
        def elo_diff(self):
            return self.elo_as_int - int(self.player.rating + 0.5)


class TeamDetails(DetailView):
    model = Team


class TeamCreate(CreateView):
    model = Team
    form_class = TeamCreateForm

    def get_initial(self):
        self.success_url = self.request.GET['next']\
            if 'next' in self.request.GET else reverse('team-list')
        initial = super(CreateView, self).get_initial()
        initial = initial.copy()

        if 'players' in self.request.GET:
            initial['players'] = [
                int(x) for x in self.request.GET['players'].split(',')]
        return initial

    def post(self, request):
        return super().post(request)

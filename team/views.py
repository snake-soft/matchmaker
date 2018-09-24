""" views of team module """
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse

from player.models import Player, Elo
from .models import Team
from .forms import TeamCreateForm


class TeamList(LoginRequiredMixin, ListView):\
        # pylint: disable=too-many-ancestors
    """ view all teams as list """
    model = Team

    def get_queryset(self):
        return Team.objects.filter(
            communities=self.request.user.active_community)


class TeamListRealtime(LoginRequiredMixin, ListView):\
        # pylint: disable=too-many-ancestors
    """ realtime list of all teams """
    model = Team
    template_name = 'team/team_list_realtime.html'

    def get_queryset(self):
        Team.set_from_to(
            self.request.session['from'], self.request.session['to'])
        return Team.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):  # pylint: disable=W0221
        context = super().get_context_data(**kwargs)
        if 'firstteam' in self.request.GET and self.request.GET['firstteam']:
            context = self.init_teams(context)
        context['max_score'] = self.max_score
        return context

    def init_teams(self, context):
        """ initialize realtime teams and add to context """
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
            context['player_realtime'][obj.pk_] = obj
        for player in secondteam.players.all():  # BEFORE TEAM REALTIME!
            obj = self.PlayerRealtimeValues(
                player,
                firstteam,
                int(self.request.GET['secondteam_goals'])
                - int(self.request.GET['firstteam_goals'])
            )
            context['player_realtime'][obj.pk_] = obj

        context['team_realtime'] = {}
        obj = self.TeamRealtimeValues(
            self.request,
            (firstteam, secondteam),
            (int(self.request.GET['firstteam_goals']),
             int(self.request.GET['secondteam_goals'])),
            context['player_realtime'],
        )
        context['team_realtime'][obj.own_team.pk] = obj
        obj = self.TeamRealtimeValues(
            self.request,
            (secondteam, firstteam),
            (int(self.request.GET['secondteam_goals']),
             int(self.request.GET['firstteam_goals'])),
            context['player_realtime'],
        )
        context['team_realtime'][obj.own_team.pk] = obj
        return context

    @property
    def max_score(self):
        return max([x.team_score for x in Team.objects.filter(
            owner=self.request.user)])

    class TeamRealtimeValues:
        """ class for realtime calculated values of teams """

        def __init__(self, request, teams, goals, player_rt):
            self.request = request
            self.own_team, enemy = teams
            self.own_goals, self.enemy_goals = goals
            self.own_team.set_from_to(
                request.session['from'],
                request.session['to']
            )
            enemy.set_from_to(
                request.session['from'],
                request.session['to']
            )
            self.player_realtimes = player_rt

        @property
        def team_score(self):
            """ returns realtime score of own_team, percent """
            score = self.own_team.team_score
            if self.own_goals > self.enemy_goals:
                score += 2
            elif self.own_goals == self.enemy_goals:
                score += 1
            return score

        @property
        def max_score(self):
            """ needs rework!!! """
            return max([x.team_score for x in Team.objects.filter(
                owner=self.request.user)])

        @property
        def team_score_percent(self):
            sum_ = max([x.team_score for x in Team.objects.filter(
                owner=self.request.user)])
            sum_ = 100 / sum_ if sum_ else 0
            return self.team_score * sum_

        @property
        def team_score_diff(self):
            """ returns difference between old and realtime score """
            return self.team_score - self.own_team.team_score

        @property
        def team_wdl(self):
            """ returns realtime values of ([win], [draw], [lose]) """
            wdl = self.own_team.get_win_draw_lose
            if self.own_goals > self.enemy_goals:
                wdl[0].append("Realtime")
            elif self.own_goals == self.enemy_goals:
                wdl[1].append("Realtime")
            elif self.own_goals < self.enemy_goals:
                wdl[2].append("Realtime")
            return wdl

        @property
        def get_win_draw_lose_percent(self):
            win, draw, lose = self.team_wdl
            sum_ = len(win) + len(draw) + len(lose)
            sum_ = 100 / sum_ if sum_ else 0
            return len(win) * sum_, len(draw) * sum_, len(lose) * sum_

        @property
        def team_wdl_diff(self):
            """ returns realtime difference of (win, draw, lose) old vs new """
            wdl = self.team_wdl
            wdl_orig = self.own_team.get_win_draw_lose
            return (
                len(wdl[0]) - len(wdl_orig[0]),
                len(wdl[1]) - len(wdl_orig[1]),
                len(wdl[2]) - len(wdl_orig[2])
            )

        @property
        def team_wdl_factor(self):
            """ len win - len lose (for sorting w:d:l) """
            return len(self.team_wdl[0]) - len(self.team_wdl[2])

        @property
        def close_wl(self):
            """ returns realtime ([close_win], [close_lose]) """
            close_wl = self.own_team.close_win_lose
            if self.own_goals - self.enemy_goals == 1:
                close_wl[0].append("Realtime")
            elif self.own_goals - self.enemy_goals == -1:
                close_wl[1].append("Realtime")
            return close_wl

        @property
        def close_win_lose_percent(self):
            win, lose = self.close_wl
            sum_ = len(win) + len(lose)
            sum_ = 100 / sum_ if sum_ else 0
            return len(win) * sum_, len(lose) * sum_

        @property
        def close_wl_factor(self):
            """ len close_win - len close_lose (for sorting close_win:lose) """
            return len(self.close_wl[0]) - len(self.close_wl[1])

        @property
        def close_wl_diff(self):
            """ returns difference of clos_win : close_lose """
            close_wl = self.close_wl
            close_wl_orig = self.own_team.close_win_lose
            return [
                len(close_wl[0]) - len(close_wl_orig[0]),
                len(close_wl[1]) - len(close_wl_orig[1])
            ]

        @property
        def realtime_goal_own_foreign(self):
            """ returns (own_goals_count : foreign_goals_count) """
            own, foreign = self.own_team.goal_own_foreign
            own += self.own_goals
            foreign += self.enemy_goals
            return own, foreign

        @property
        def goal_own_foreign_diff(self):
            own, foreign = self.realtime_goal_own_foreign
            own_orig, foreign_orig = self.own_team.goal_own_foreign
            return own - own_orig, foreign - foreign_orig

        @property
        def goal_own_foreign_percent(self):
            own, foreign = self.realtime_goal_own_foreign
            sum_ = own + foreign
            sum_ = 100 / sum_ if sum_ else 0
            return own * sum_, foreign * sum_

        @property
        def goal_factor(self):
            """ own_goals vs enemy_goals """
            return self.realtime_goal_own_foreign[0] \
                - self.realtime_goal_own_foreign[1]

        @property
        def strength(self):
            """ new realtime strength of team """
            tmp = []
            for player in self.own_team.players.all():
                for player_rt in self.player_realtimes.values():
                    if player.pk == player_rt.player.pk:
                        tmp.append(player_rt.elo)
            return int(sum(tmp) / len(tmp) + 0.5)

        @property
        def strength_diff(self):
            """ difference of old vs realtime strength """
            return self.strength - int(self.own_team.team_rating + 0.5)

    class PlayerRealtimeValues:
        """ class for realtime calculated values of players """

        def __init__(self, player, enemy_team, goal_diff):
            self.player = player
            self.pk_ = player.pk
            self.enemy_team = enemy_team
            self.goal_diff = goal_diff
            self.elo = self._new_elo()

        def _new_elo(self):
            elo = Elo(self.player.rating)
            return elo.new_result(
                self.enemy_team.team_rating,
                self.goal_diff
            )

        @property
        def elo_diff(self):
            """ new realtime elo """
            return self.elo_as_int - int(self.player.rating + 0.5)

        @property
        def elo_as_int(self):
            """ new realtime elo as int """
            return int(self.elo + 0.5)


class TeamDetails(LoginRequiredMixin, DetailView):\
        # pylint: disable=too-many-ancestors
    """ View details of one team """
    model = Team

    def get_queryset(self):
        return Team.objects.filter(owner=self.request.user)


class TeamCreate(LoginRequiredMixin, CreateView):\
        # pylint: disable=too-many-ancestors
    """ view for creating new team """
    model = Team
    form_class = TeamCreateForm

    def get_initial(self):
        self.success_url = self.request.GET['next']\
            if 'next' in self.request.GET else reverse('team-list')
        initial = super().get_initial()
        initial = initial.copy()
        if 'players' in self.request.GET:
            initial['players'] = [
                int(x) for x in self.request.GET['players'].split(',')]
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        self.success_url = self.request.POST.get('next', reverse('ladder'))
        valid = False
        teamname = form.cleaned_data['teamname']
        owner = self.request.user
        form.instance.owner = owner
        existing_team = self.model.players_have_team(
            [Player.objects.get(pk=int(x), owner=owner)
             for x in self.request.POST.getlist('players')]
        )
        teamname_exists = Team.objects.filter(
            teamname__iexact=teamname,
            owner=owner
        )
        if existing_team:
            form.errors['error'] = \
                str(existing_team) + ' constellation already exists'
        elif teamname_exists and teamname:
            form.errors['error'] = \
                str(teamname_exists[0]) + ' team already exists'
        else:
            valid = True
        return super().form_valid(form) if valid \
            else super().form_invalid(form)

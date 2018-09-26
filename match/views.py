""" views of match module """
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from .models import Match
from .forms import MatchCreateForm


class MatchList(LoginRequiredMixin, ListView):\
        # pylint: disable=too-many-ancestors
    """ View List of matches """
    model = Match

    def get_queryset(self):
        if 'from' in self.request.session:
            frm = self.request.session['from']
        else:
            frm = '2000-01-01'

        if 'to' in self.request.session:
            to_ = datetime.strptime(
                self.request.session['to'], '%Y-%m-%d').date()
            to_ += timedelta(days=1)
            to_ = to_.strftime('%Y-%m-%d')
        else:
            to_ = '3000-01-01'
        return Match.objects.filter(
            date_time__range=[frm, to_],
            #owner=self.request.user
        )


class MatchDetails(LoginRequiredMixin, DetailView):\
        # pylint: disable=too-many-ancestors
    """ View Details of a single view """
    model = Match

    def get_queryset(self):
        Match.set_from_to(
            self.request.session['from'], self.request.session['to'])
        return Match.objects.filter() #owner=self.request.user)


class MatchCreate(LoginRequiredMixin, CreateView):\
        # pylint: disable=too-many-ancestors
    """ create new match-form"""
    model = Match
    form_class = MatchCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        #kwargs['owner'] = self.request.user
        return kwargs

    def get_initial(self):
        self.success_url = self.request.path
        initial = super().get_initial()
        initial = initial.copy()

        initial['firstteam'] = self.request.session['last_firstteam'] \
            if 'last_firstteam' in self.request.session \
            else ''

        initial['secondteam'] = self.request.session['last_secondteam'] \
            if 'last_secondteam' in self.request.session \
            else ''

        if 'firstteam' in self.request.GET:
            initial['firstteam'] = int(self.request.GET['firstteam'])
        if 'secondteam' in self.request.GET:
            initial['secondteam'] = int(self.request.GET['secondteam'])
        return initial

    def form_valid(self, form):
        #=======================================================================
        # owner = self.request.user
        # form.instance.owner = owner
        #=======================================================================
        valid = False
        if form.cleaned_data['firstteam_goals'] \
                == 0 and form.cleaned_data['secondteam_goals'] == 0:
            form.errors['error'] = 'Score cannot be 0:0'
        elif form.cleaned_data['firstteam'] == form.cleaned_data['secondteam']:
            form.errors['error'] = 'Choose different teams!'
        else:
            self.request.session['last_firstteam'] = \
                int(self.request.POST['firstteam'])
            self.request.session['last_secondteam'] = \
                int(self.request.POST['secondteam'])
            valid = True

        return super().form_valid(form) if valid else \
            super().form_invalid(form)

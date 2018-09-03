from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from datetime import datetime, timedelta

from .models import Match
from .forms import MatchCreateForm


class MatchList(LoginRequiredMixin, ListView):
    model = Match

    def get_queryset(self):
        if 'from' in self.request.session:
            frm = self.request.session['from']
        else:
            frm = '2000-01-01'

        if 'to' in self.request.session:
            to = datetime.strptime(
                self.request.session['to'], '%Y-%m-%d').date()
            to += timedelta(days=1)
            to = to.strftime('%Y-%m-%d')
        else:
            to = '3000-01-01'
        return Match.objects.filter(
            date_time__range=[frm, to],
            owner=self.request.user
        )


class MatchDetails(LoginRequiredMixin, DetailView):
    model = Match

    def get_queryset(self):
        return Match.objects.filter(owner=self.request.user)


class MatchCreate(LoginRequiredMixin, CreateView):
    model = Match
    form_class = MatchCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_initial(self):
        self.success_url = self.request.path
        initial = super(CreateView, self).get_initial()
        initial = initial.copy()

        initial['firstteam'] = self.request.session['last_firstteam'] \
            if 'last_firstteam' in self.request.session else ''

        initial['secondteam'] = self.request.session['last_secondteam'] \
            if 'last_secondteam' in self.request.session else ''

        if 'firstteam' in self.request.GET:
            initial['firstteam'] = int(self.request.GET['firstteam'])
        if 'secondteam' in self.request.GET:
            initial['secondteam'] = int(self.request.GET['secondteam'])
        return initial

    def form_valid(self, form, *args, **kwargs):
        owner = self.request.user
        form.instance.owner = owner
        if form.cleaned_data['firstteam_goals'] \
                == 0 and form.cleaned_data['secondteam_goals'] == 0:
            form.errors['error'] = 'Score cannot be 0:0'
            return super().form_invalid(form, *args, **kwargs)

        if form.cleaned_data['firstteam'] == form.cleaned_data['secondteam']:
            form.errors['error'] = 'Choose different teams!'
            return super().form_invalid(form, *args, **kwargs)

        else:
            self.request.session['last_firstteam'] = \
                int(self.request.POST['firstteam'])
            self.request.session['last_secondteam'] = \
                int(self.request.POST['secondteam'])
            return super().form_valid(form, *args, **kwargs)

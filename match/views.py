from django.views.generic import ListView, DetailView, CreateView
from datetime import datetime, timedelta

from .models import Match


class MatchList(ListView):
    model = Match

    def get_queryset(self):
        if 'from' in self.request.session:
            frm = self.request.session['from']
        else:
            frm = '2000-01-01'

        if 'to' in self.request.session:
            to = datetime.strptime(self.request.session['to'], '%Y-%m-%d').date()
            to += timedelta(days=1)
            to = to.strftime('%Y-%m-%d')
        else:
            to = '3000-01-01'
        return Match.objects.filter(date_time__range=[frm, to])


class MatchDetails(DetailView):
    model = Match


class MatchCreate(CreateView):
    model = Match
    fields = ['firstteam', 'secondteam', 'firstteam_goals', 'secondteam_goals']

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

    def post(self, request):
        request.session['last_firstteam'] = int(request.POST['firstteam'])
        request.session['last_secondteam'] = int(request.POST['secondteam'])
        return super().post(request)

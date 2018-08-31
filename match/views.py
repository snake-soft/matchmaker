from django.views.generic import ListView, DetailView, CreateView
from datetime import datetime

from .models import Match


class MatchList(ListView):
    model = Match

    def get_queryset(self):
        frm = self.request.session['from']
        to = self.request.session['to']
        #=======================================================================
        # to = datetime.strptime(self.request.session['to'], '%Y-%m-%d').date()
        # try:
        #     to = to.replace(day=to.day+1).strftime('%Y-%m-%d')
        # except ValueError:
        #     to = to.replace(day=to.month+1).strftime('%Y-%m-%d')
        #=======================================================================
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

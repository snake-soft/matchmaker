from django.views.generic import ListView, DetailView, CreateView

from .models import Match


class MatchList(ListView):
    model = Match


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
        return initial

    def post(self, request):
        request.session['last_firstteam'] = int(request.POST['firstteam'])
        request.session['last_secondteam'] = int(request.POST['secondteam'])
        return super().post(request)
        # import pdb; pdb.set_trace()  # <---------
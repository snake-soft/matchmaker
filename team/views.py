from django.views.generic import ListView, DetailView, CreateView

from .models import Team


class TeamList(ListView):
    model = Team


class TeamDetails(DetailView):
    model = Team


class TeamCreate(CreateView):
    model = Team
    fields = ['teamname', 'players']

    def get_initial(self):
        self.success_url = self.request.path

    def post(self, request):
        return super().post(request)

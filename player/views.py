from django.views.generic import ListView, DetailView, CreateView

from .models import Player


class PlayerList(ListView):
    model = Player


class PlayerDetails(DetailView):
    model = Player

class PlayerCreate(CreateView):
    model = Player
    fields = ['nick']

    def get_initial(self):
        self.success_url = self.request.path

    def post(self, request):
        return super().post(request)

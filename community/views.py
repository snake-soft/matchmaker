from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Community


class CommunityCreate (LoginRequiredMixin, CreateView):
    model = Community


class CommunityView (LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        if request.user in request.user.active_community.gamemasters:
            pass # adminview
        else:
            pass #userview
        request.user.active_community.players
        #context['']=
        return render(
            request,
            template_name="community/manage.html",
            context=context,
        )
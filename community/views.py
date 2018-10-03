from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Community
from .forms import ManageCommunityForm
from player.models import Player


class CommunityView (LoginRequiredMixin, View):
    def get(self, request):
        ManageCommunityForm.base_fields['select_form'].choices = \
            [(x.pk, x) for x in request.user.communities.all()]
        ManageCommunityForm.base_fields['select_form'].initial = \
            request.user.active_community.pk if request.user.active_community else ""

        ManageCommunityForm.base_fields['players'].choices = \
            [(x.pk, x) for x in Player.objects.all()]
        if request.user.active_community:
            ManageCommunityForm.base_fields['players'].initial = \
                [x.pk for x in request.user.active_community.players]

        return render(request, template_name="community/manage.html",
            context={'community_manage': ManageCommunityForm},)

    def post(self, request):
        form = ManageCommunityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            if form.cleaned_data.get('select_form'):
                request.user.active_community = Community.objects.get(pk=int(
                    form.cleaned_data.get('select_form')))
                request.user.save()

            if form.cleaned_data.get('players'):
                playerlist = form.cleaned_data.get('players')
                request.user.active_community.set_players(Player.objects.filter(id__in=[int(x)for x in form.cleaned_data.get('players')]))

            #===================================================================
            # for player in Player.objects.filter(
            #         id__in=[int(x)for x in form.cleaned_data.get('players')]):
            #     if player not in request.user.active_community.players:
            #         CommunityMembership(community=request.user.active_community, member=player)
            # for player in request.user.active_community.players:
            #     membership = player.get_communitymembership(
            #         request.user.active_community)
            #     if player.pk not in form.cleaned_data.get('players'):
            #         [x.delete() for x in CommunityMembership.objects.filter(community=request.user.active_community, member=player) if not x.owner and not x.gamemaster]
            #===================================================================




            # request.user.active_community in Player.objects.filter(id__in=[int(x) for x in form.cleaned_data.get('players')])[0].communities.all()
            #request.user.active_community.player_set(Player.objects.filter(id__in=[int(x) for x in form.cleaned_data.get('players')]))
            #===================================================================
            # request.user.active_community.teams_set = Team.objects.filter(
            #     id__in=[int(x) for x in form.cleaned_data.get('teams')])
            #===================================================================
        else:
            print(form.errors)
        return redirect(request.POST.get('next', '/'))
            
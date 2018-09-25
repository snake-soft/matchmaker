from django import forms

from .models import Community
from core.models import PlayerTeamBase
from team.models import Team
from player.models import Player



class ManageCommunityForm(forms.Form):
    select_form = forms.ChoiceField(widget=forms.Select(
        attrs={'onchange': 'this.form.submit();'}), required=False,)

    #===========================================================================
    # teams = forms.MultipleChoiceField(required=False,
    #     widget=forms.CheckboxSelectMultiple(
    #         attrs={'onchange': 'this.form.submit();'}))
    #===========================================================================

    players = forms.MultipleChoiceField(required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'onchange': 'this.form.submit();'}))

    #===========================================================================
    # def __init__(self, request, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if request.user.active_community:
    #         self.teams.initial = request.user.active_community.teams
    #         self.teams.initial = request.user.active_community.players
    #===========================================================================
    

    #===========================================================================
    # class Meta:
    #     model = Community
    #     fields = ['name']
    #===========================================================================



class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name']

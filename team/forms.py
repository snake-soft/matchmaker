""" team forms """
from django import forms

from player.models import Player
from .models import Team


class TeamCreateForm(forms.ModelForm):
    """ Team creation form """

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = Player.objects.filter(owner=owner)

    class Meta:
        model = Team
        fields = ['teamname', 'players']
        widgets = {'players': forms.CheckboxSelectMultiple()}

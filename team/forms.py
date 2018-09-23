""" team forms """
from django import forms

from player.models import Player
from .models import Team


class TeamCreateForm(forms.ModelForm):
    """ Team creation form """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = Player.objects.filter(
            owner=self.request.user if self.request.user.is_authenticated
            else False)

    class Meta:
        model = Team
        fields = ['teamname', 'players']
        widgets = {'players': forms.CheckboxSelectMultiple()}

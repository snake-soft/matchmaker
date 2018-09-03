from django import forms
from .models import Team
from player.models import Player


class TeamCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super().__init__(*args, **kwargs)
        self.fields['players'].queryset = Player.objects.filter(owner=owner)

    class Meta:
        model = Team
        fields = ['teamname', 'players']
        widgets = {'players': forms.CheckboxSelectMultiple()}

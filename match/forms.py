""" match forms """
from django import forms

from team.models import Team
from player.models import Player
from .models import Match


class MatchCreateForm(forms.ModelForm):
    """ match creation form """

    def __init__(self, *args, **kwargs):
        #owner = kwargs.pop('owner')
        super().__init__(*args, **kwargs)
        self.fields['firstteam'].queryset = Team.objects.filter() #owner=owner
        self.fields['secondteam'].queryset = Team.objects.filter()#owner=owner

    class Meta:
        model = Match
        fields = [
            'firstteam',
            'secondteam',
            'firstteam_goals',
            'secondteam_goals',
        ]

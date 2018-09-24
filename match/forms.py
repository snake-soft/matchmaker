""" match forms """
from django import forms

from team.models import Team
from .models import Match


class MatchCreateForm(forms.ModelForm):
    """ match creation form """

    def __init__(self, *args, **kwargs):
        community = kwargs.pop('community')
        super().__init__(*args, **kwargs)

        self.fields['firstteam'].queryset = \
            Team.objects.filter(communities=community)

        self.fields['secondteam'].queryset = \
            Team.objects.filter(communities=community)

    class Meta:
        model = Match
        fields = [
            'firstteam',
            'secondteam',
            'firstteam_goals',
            'secondteam_goals',
        ]

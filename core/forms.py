from django.forms import ModelForm, inlineformset_factory

from match.models import Match
from team.models import Team
from player.models import Player


class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = ['firstteam', 'secondteam', 'firstteam_goals', 'secondteam_goals']


TeamForm = inlineformset_factory(Match, Team)
PlayerForm = inlineformset_factory(Match, Player)

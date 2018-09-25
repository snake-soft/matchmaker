""" team forms """
from django import forms

from player.models import Player
from .models import Team


class CheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, attrs=None, choices=()):
        forms.CheckboxSelectMultiple.__init__(self, attrs=attrs, choices=choices)

    def id_for_label(self, id_, index=None):
        id_ += '_nav'
        return forms.CheckboxSelectMultiple.id_for_label(self, id_, index=index)


class TeamCreateForm(forms.ModelForm):
    """ Team creation form """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated and user.active_community:
            self.fields['players'].queryset = user.active_community.players
        else:
            self.fields['players'].queryset = Player.objects.none()
        #=======================================================================
        # else:
        #     self.fields['players'].queryset = ''
        #=======================================================================

    class Meta:
        model = Team
        fields = ['name', 'players']
        widgets = {'players': CheckboxSelectMultiple()}

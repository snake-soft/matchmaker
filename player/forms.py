""" player forms """
from django import forms

from player.models import Player


class PlayerCreateForm(forms.ModelForm):
    """ Team creation form """
    model = Player
    fields = ['nick']

    class Meta:
        model = Player
        fields = ['nick']

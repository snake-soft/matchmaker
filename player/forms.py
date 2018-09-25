""" player forms """
from django import forms

from player.models import Player
#from .models import Team


class PlayerCreateForm(forms.ModelForm):
    """ Team creation form """
    model = Player
    fields = ['nick']

    def clean(self):
        import pdb; pdb.set_trace()  # <---------
        #=======================================================================
        # name = self.cleaned_data['nick']
        # owner = self.request.user
        # self.instance.owner = owner
        # player_exists = Player.objects.filter(nick__iexact=name, owner=owner)
        # team_exists = Team.objects.filter(teamname__iexact=name, owner=owner)
        # if player_exists or team_exists:
        #     self.errors['error'] = name + ' already exists'
        #     return super().form_invalid(self)
        #=======================================================================
        return super().clean(self)

    def get_initial(self):
        self.success_url = self.request.POST.get('next', '/')

    class Meta:
        model = Player
        fields = ['name']

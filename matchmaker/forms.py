from django import forms

from player.models import Player


class MatchmakerForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = sorted(
            Player.objects.filter(owner=request.user),
            key=lambda x: x.rating,
            reverse=True
            )
        choices = tuple((x.pk, "%s (%s)" % (x.nick, x.rating_as_int))
                        for x in (choices))
        initial = request.session['last_players'] \
            if len(request.session['last_players']) is True else ''
        self.fields['players'] = forms.MultipleChoiceField(
            choices=choices,
            widget=forms.CheckboxSelectMultiple,
            initial=initial,
            )
        initial = int(request.session['last_count']) \
            if request.session['last_count'] else 2
        self.fields['count'] = forms.ChoiceField(
            label="Constellation",
            choices=[
                [2, '1 vs 1'],
                [3, '2 vs 1'],
                [4, '2 vs 2'],
                [5, '3 vs 2'],
                [6, '3 vs 3'],
                ],
            widget=forms.RadioSelect(attrs={}),
            initial=initial,
            )

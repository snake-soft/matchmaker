from django import forms #import Form, ModelForm, inlineformset_factory, DateField


class TimeRangeForm(forms.Form):
    def __init__(self, request):
        super().__init__()
        self.fields["from"] = forms.DateField(
            widget=forms.DateInput(attrs={"data-toggle": "datepicker"}),
            initial=request.session["from"],
            )
        self.fields["to"] = forms.DateField(
            widget=forms.DateInput(attrs={"data-toggle": "datepicker"}),
            initial=request.session["to"]
            )


#===============================================================================
# class MatchForm(forms.ModelForm):
#     class Meta:
#         model = Match
#         fields = ['firstteam', 'secondteam', 'firstteam_goals', 'secondteam_goals']
# 
# 
# TeamForm = forms.inlineformset_factory(Match, Team)
# PlayerForm = forms.inlineformset_factory(Match, Player)
#===============================================================================
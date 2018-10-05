from django import forms

from .models import Community


class ManageCommunityForm(forms.Form):
    select_form = forms.ChoiceField(widget=forms.Select(
        attrs={'onchange': 'this.form.submit();'}), required=False,)

    owner = forms.CharField(widget=forms.TextInput(attrs={'disabled': 'True'}), required=False)

    players = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple(
            attrs={'onchange': 'this.form.submit();'}))

    gamemasters = forms.MultipleChoiceField(
        required=False, widget=forms.CheckboxSelectMultiple(
            attrs={'onchange': 'this.form.submit();'}))


class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name']

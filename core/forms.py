""" forms of core module """
from django import forms


class TimeRangeForm(forms.Form):
    """ form of date setter """
    frm = forms.DateField(
        widget=forms.DateInput(attrs={"data-toggle": "datepicker", }),
        )
    to = forms.DateField(
        widget=forms.DateInput(attrs={"data-toggle": "datepicker", }),
        )

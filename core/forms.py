from django import forms


class TimeRangeForm(forms.Form):
    frm = forms.DateField(
        widget=forms.DateInput(attrs={"data-toggle": "datepicker", }),
        )
    to = forms.DateField(
        widget=forms.DateInput(attrs={"data-toggle": "datepicker", }),
        )
    
    #===========================================================================
    # def __init__(self, request, *args, **kwargs):
    #     super().__init__(request, *args, **kwargs)
    #     self.fields["from"] = forms.DateField(
    #         widget=forms.DateInput(attrs={"data-toggle": "datepicker", }),
    #         initial=request.session["from"],
    #         )
    #     self.fields["to"] = forms.DateField(
    #         widget=forms.DateInput(attrs={"data-toggle": "datepicker", }),
    #         initial=request.session["to"]
    #         )
    #===========================================================================

from django import forms


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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from .forms import TimeRangeForm


class StartView(View):
    def get(self, request):
        return render(request, template_name="home.html")


class DateSetView(LoginRequiredMixin, View):  # Form Validation MISSING!!!
    def post(self, request):
        form = TimeRangeForm(request.POST)
        if form.is_valid()\
                and form.cleaned_data['frm'] <= form.cleaned_data['to']:
            request.session['from'] = form.cleaned_data['frm'].strftime(
                '%Y-%m-%d')
            request.session['to'] = form.cleaned_data['to'].strftime(
                '%Y-%m-%d')
        nxt = request.POST.get('next', '/')
        return HttpResponseRedirect(nxt)

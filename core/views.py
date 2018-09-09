""" core views """
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect
from django.views import View

from .forms import TimeRangeForm


class StartView(View):
    """ start view (home) """
    def get(self, request):
        """ get view """
        return render(request, template_name="home.html")


class DateSetView(LoginRequiredMixin, View):
    """ date setter """
    def post(self, request):
        """ post view """
        form = TimeRangeForm(request.POST)
        if form.is_valid()\
                and form.cleaned_data['frm'] <= form.cleaned_data['to']:
            request.session['from'] = form.cleaned_data['frm'].strftime(
                '%Y-%m-%d')
            request.session['to'] = form.cleaned_data['to'].strftime(
                '%Y-%m-%d')
        nxt = request.POST.get('next', '/')
        return HttpResponseRedirect(nxt)

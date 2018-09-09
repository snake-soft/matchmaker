""" views of account """
from django.shortcuts import redirect
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


class SignUpView(FormView):
    """ Signup new users """
    form_class = UserCreationForm
    template_name = 'account/signup.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('home')

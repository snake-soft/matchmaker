""" views of account """
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model


class SignUpView(generic.FormView):
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


class AccountView(generic.UpdateView):
    # form_class = AccountViewForm
    template_name = 'account/account.html'
    model = get_user_model()
    success_url = '/'
    fields = ['nick', 'email', 'active_community']

    def get_object(self, queryset=None):
        return self.request.user

""" views of account """
from django.views.generic import FormView, UpdateView
from django.contrib.auth import get_user_model

from account.forms import AccountCreationForm


class SignUpView(FormView):
    form_class = AccountCreationForm
    template_name = 'account/signup.html'
    success_url = '/'


class AccountView(UpdateView):
    # form_class = AccountViewForm
    template_name = 'account/account.html'
    model = get_user_model()
    success_url = '/'
    fields = ['nick', 'email', 'active_community']

    def get_object(self, queryset=None):
        return self.request.user

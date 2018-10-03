""" views of account """
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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
    fields = ['name', 'email', 'active_community']

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST)
        form.is_valid()
        import pdb; pdb.set_trace()  # <---------
        return generic.UpdateView.post(self, request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        self.extra_context = {'pw_form': PasswordChangeForm(user=self.request.user)}
        return generic.UpdateView.get_context_data(self, **kwargs)

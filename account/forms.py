from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from django.contrib.auth import get_user_model


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'nick']
        labels = {'username': 'Username (for login)'}

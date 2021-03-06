from django import forms
from django.contrib.auth.forms import UserCreationForm

from dark.models.user import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Required. Please enter valid email.")
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

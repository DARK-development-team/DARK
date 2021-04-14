from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login

from dark.forms.user import UserRegistrationForm


class UserRegistrationView(CreateView):
    template_name = 'dark/user/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home:page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:page')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        valid = super(UserRegistrationView, self).form_valid(form)

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)

        return valid

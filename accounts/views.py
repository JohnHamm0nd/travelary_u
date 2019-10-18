from django.shortcuts import render
from django.views.generic import CreateView
from . import forms
from django.urls import reverse_lazy
# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:signin')
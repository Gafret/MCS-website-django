from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password

from .forms import SignUpForm

# Create your views here.
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "authentication/signup_page.html"
    model = User
    success_url = reverse_lazy('articles:home')

    def form_valid(self, form):
        form.instance.password = make_password(self.request.POST['password'])
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'authentication/login_page.html'
    model = User

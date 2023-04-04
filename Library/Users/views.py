from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout
# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm


def register_request(request):
    if request.method == "POST":
        print(request.POST)
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("register")
    form = NewUserForm()
    return render(request, "register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home_page")
            else:
                return redirect("login_user")
        else:
            return redirect("login_user")

    form = AuthenticationForm() 
    return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
    logout(request)
    return redirect("login_user")

from django.views.generic import View
from django.contrib.auth import forms

class LoginPageView(View):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def get(self, request):
        # print('in get method')
        form = self.form_class()
        return render(request, self.template_name, context={'login_form':form})

    def post(self, request):
        # print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            print('in valid method')
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home_page')
        return render(request, self.template_name, context={'login_form':form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect ("login_user")
# https://ordinarycoders.com/blog/article/django-user-register-login-logout


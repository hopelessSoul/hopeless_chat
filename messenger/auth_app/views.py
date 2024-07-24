from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from auth_app.forms import SignUpForm, SignInForm
from auth_app.models import Profile


class LoggedInUser(View):
    def get(self, request):
        user = request.user
        print(user)
        return render(request, 'auth/logged-in.html', {"user": user})


class SignUpView(View):
    def post(self, request):
        form = SignUpForm(request.POST)
        success_url = reverse_lazy('auth_app:current_user')
        try:
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.validate_email()
                username = form.validate_username()
                password = form.validate_password()
                user = form.save()
                login(request, user)
                authenticate(username=username, password=password)
                profile = Profile(email=email, name=name, username=username)
                profile.save()
                return HttpResponseRedirect(success_url)
            raise Exception
        except Exception as ex:
            error_url = reverse_lazy('auth_app:sign_up')
            return HttpResponseRedirect(error_url)

    def get(self, request):
        form = SignUpForm()
        return render(request, "auth/sign_up.html", {"form": form})


class SingInView(View):
    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.validate_user()
            print(user)
            login(request, user)
            print(request.user.username)
            return redirect('/')

    def get(self, request):
        form = SignInForm()
        return render(request, "auth/sign_in.html", {"form": form})


class SignOutView(View):
    def post(self, request):
        logout(request)
        return redirect('/')

    def get(self, request):
        return render(request, 'auth/logout.html', {})

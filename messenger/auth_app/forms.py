from django import forms
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=50)
    name = forms.CharField(min_length=2, max_length=100, label="Name")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def validate_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if user.count():
            return None
        return username

    def validate_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2 or (not password2 or password1):
            return None
        return password1

    def validate_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user.count():
            return None
        return email

    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user


class SignInForm(forms.Form):
    username = forms.CharField(label='Your username', min_length=3, max_length=50)
    password = forms.CharField(label='Your password', widget=forms.PasswordInput)

    def validate_user(self):
        password = self.cleaned_data['password']
        username = self.validate_username()
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            return user
        return None

    def validate_username(self):
        username = self.cleaned_data['username']
        user = User.objects.get(username=username)
        if user:
            return username
        return None

# Create your views here.
import json
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password, check_password
from spendingtrackers.models import User
from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    first_name = forms.CharField(label='first_name', max_length=50)
    last_name = forms.CharField(label='last_name', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='password_confirmation', widget=forms.PasswordInput())


def sign_up(request):
    if request.method == 'POST':
        userform = SignUpForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            first_name = userform.cleaned_data['first_name']
            last_name = userform.cleaned_data['last_name']
            password = userform.cleaned_data['password']
            password_confirmation = userform.cleaned_data['password_confirmation']
            if password != password_confirmation:
                messages.add_message(request, messages.ERROR, "The two passwords are inconsistent!")
                return render(request, 'sign_up.html')
            try:
                user = User()
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.password = make_password(password)
                user.save()
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, "email already exists!")
                return render(request, 'sign_up.html')

            return render(request, 'sign_success.html')
        else:
            return render(request, 'sign_up.html')
    else:
        return render(request, 'sign_up.html')


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


def login(request):
    if request.method == 'POST':
        userform = LoginForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            user = User.objects.filter(username__exact=username).first()

            if not user or not check_password(password, user.password):
                messages.add_message(request, messages.ERROR, "Account or password error!")
                return render(request, 'log_in.html')
            else:
                request.session['is_login'] = True
                request.session['username'] = username

                return render(request, 'feed.html')

        else:
            return render(request, 'log_in.html')
    else:
        return render(request, 'log_in.html')


def home_page(request):
    return render(request, 'home_page.html')


def feed(request):
    if not request.session.get('is_login'):
        return render(request, 'log_in.html')
    return render(request, 'feed.html')


def sign_success(request):
    if not request.session.get('is_login'):
        return render(request, 'log_in.html')
    return render(request, 'sign_success.html')


def log_out(request):
    if not request.session.get('is_login'):
        return render(request, 'log_in.html')
    del request.session['is_login']
    del request.session['username']
    return redirect('home_page')


class ChangePasswordForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    his_password = forms.CharField(label='his_password', widget=forms.PasswordInput())
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='password_confirmation', widget=forms.PasswordInput())


def change_password(request):
    if request.method == 'POST':
        userform = ChangePasswordForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            his_password = userform.cleaned_data['his_password']
            password = userform.cleaned_data['password']
            password_confirmation = userform.cleaned_data['password_confirmation']
            if password != password_confirmation:
                messages.add_message(request, messages.ERROR, "The two passwords are inconsistent!")
                return render(request, 'change_password.html')
            user = User.objects.filter(username__exact=username).first()
            if not user:
                messages.add_message(request, messages.ERROR, "email not exists!")
                return render(request, 'change_password.html')
            if not check_password(his_password, user.password):
                messages.add_message(request, messages.ERROR, "history password error!")
                return render(request, 'change_password.html')
            user.password = make_password(password)
            user.save()
            return render(request, 'log_in.html')
        else:
            return render(request, 'change_password.html')
    else:
        return render(request, 'change_password.html')

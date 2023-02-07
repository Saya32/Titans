from django import forms
from .models import User, Transaction
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.forms import UserChangeForm

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user

class SignUpForm(forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'currency']
        labels = {
            'username': 'Email',
        }


    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            password=self.cleaned_data.get('new_password'),
            currency=self.cleaned_data.get('currency'),
        )
        return user


class UserForm(forms.ModelForm):
    

    """Form to update user profiles."""
    class Meta:

        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'currency', 'username']
        


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'description', 'amount', 'date_paid', 'time_paid', 'category', 'receipt', 'transaction_type']
        labels = {
            'title': ('Title:'),
            'description': ('Description'),
            'amount': ('Amount:'),
            'date_paid': ('Date:'),
            'time_paid': ('Time:'),
            'category': ('Category:'),
            'receipt': ('Receipt:'),
            'transaction_type': ('Transaction type:'),

        }


    """Override clean method to check date and time"""
    def clean(self):
        super().clean()
        # date = self.cleaned_data.get('date_paid')
        # if (date == None):
        #     self.add_error('date','Please enter the date as YYYY-MM-DD.')
        #     return

        # time = self.cleaned_data.get('time_paid')
        # if (time == None):
        #     self.add_error('time','Please enter the time as HH:MM.')
        #     return

        # if(date <= timezone.now().date()):
        #     self.add_error('date','Date must be in the future.')
        #     if (date == timezone.now().date() and time <= timezone.now().time()):
        #         self.add_error('time','Time must be in the future.')

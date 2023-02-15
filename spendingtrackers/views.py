# Create your views here.
import json
from django.shortcuts import render, redirect
from .models import User, Transaction, Category
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .forms import SignUpForm, LogInForm, CategoryDetailsForm, ChangePasswordForm, UserForm, TransactionForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import  UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .helpers import get_user_transactions
from django.contrib.auth.hashers import make_password, check_password
#from spendingtrackers.models import User
#from django import forms


# class SignUpForm(forms.Form):
#     username = forms.CharField(label='username', max_length=50)
#     first_name = forms.CharField(label='first_name', max_length=50)
#     last_name = forms.CharField(label='last_name', max_length=50)
#     password = forms.CharField(label='password', widget=forms.PasswordInput())
#     password_confirmation = forms.CharField(label='password_confirmation', widget=forms.PasswordInput())


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """View that handles log in."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = 'feed'

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)

        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


class SignUpView(LoginProhibitedMixin, FormView):
    """View that signs up user."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


def home_page(request):
    return render(request, 'home_page.html')


def feed(request):
    return render(request, 'feed.html')


def sign_success(request):
    if not request.session.get('is_login'):
        return render(request, 'log_in.html')
    return render(request, 'sign_success.html')


def log_out(request):
    logout(request)
    return redirect('home_page')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    """View to update logged-in user's profile."""
    model = UserForm
    template_name = "profile.html"
    form_class = UserForm



    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user


    def get_success_url(self):
        """Return redirect URL after successful update."""
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            Transaction.objects.create(
                user=request.user,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                amount=form.cleaned_data.get('amount'),
                date_paid=form.cleaned_data.get('date_paid'),
                time_paid=form.cleaned_data.get('time_paid'),
                category=form.cleaned_data.get('category'),
                receipt=form.cleaned_data.get('receipt'),
                transaction_type=form.cleaned_data.get('transaction_type')
            )
            return redirect('feed')
        else:
            return render(request, 'new_transaction.html', {'form': form})
    else:
        form = TransactionForm()
        return render(request, 'new_transaction.html', {'form': form})


def records(request):
    transactions = get_user_transactions(request.user)
    return render(request, 'records.html', {'transactions' : transactions})

def update_record(request, id):
    try:
        record = Transaction.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Record could not be found!")
        return redirect('feed')

    if request.method == 'POST':
        form = TransactionForm(instance = record, data = request.POST)
        if (form.is_valid()):
            messages.add_message(request, messages.SUCCESS, "Record updated!")
            form.save()
            return redirect('feed')
        else:
            return render(request, 'update_record.html', {'form': form, 'transaction' : record})
    else:
        form = TransactionForm(instance = record)
        return render(request, 'update_record.html', {'form': form, 'transaction' : record})

def delete_record(request, id):
    if (Transaction.objects.filter(pk=id)):
        Transaction.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your record.")
        return redirect('feed')

def add_category_details(request):
    if request.method == 'POST':
        form = CategoryDetailsForm(request.POST)
        if form.is_valid():
            Category.objects.create(
                user=request.user,
                spending_limit=form.cleaned_data.get('spending_limit'),
                category_choices=form.cleaned_data.get('category_choices'),
                budget=form.cleaned_data.get('budget'),
                start_date=form.cleaned_data.get('start_date'),
                end_date=form.cleaned_data.get ('end_date')
            )
        else:
            return render(request, 'add_category_details.html', {'form': form})
    else:
        form = CategoryDetailsForm()
        return render(request, 'add_category_details.html', {'form': form})


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

def category(request):
   CATEGORY_CHOICES = Category.CATEGORY_CHOICES
   return render(request, 'category.html', {'CATEGORY_CHOICES':CATEGORY_CHOICES})


def view_category(request, category_id):
    category = Category.objects.get(category_id=category_id)
    return render(request, 'view_category.html', {'category':category})
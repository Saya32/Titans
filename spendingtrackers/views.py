# Create your views here.
from django.shortcuts import render, redirect
from .models import User, Transaction, Category
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LogInForm, SpendingLimitForm
from django.contrib.auth import login, logout
##from .decorators import student_required, director_required, admin_required
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import  UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, TransactionForm

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
        form = TransactionForm(request.POST)
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
            #return redirect('feed')
        else:
            return render(request, 'new_transaction.html', {'form': form})
    else:
        form = TransactionForm()
        return render(request, 'new_transaction.html', {'form': form})

def spending_limit(request):
    if request.method == 'POST':
        form = SpendingLimitForm(request.POST)
        if form.is_valid():
            Limit.objects.create(
                user=request.user,
                spending_limit=form.cleaned_data.get('spending_limit'),
                category_choices=form.cleaned_data.get('category_choices')
            )
        else:
            return render(request, 'spending_limit.html', {'form': form})
    else:
        form = SpendingLimitForm()
        return render(request, 'spending_limit.html', {'form': form})

# Create your views here.
from .delete_lesson_request import LessonRequestDeleteView
from .home import home
from .log_in import log_in
from .log_out import log_out
from .sign_up import sign_up
from .update_lesson_request import LessonRequestUpdateView
from .view_lesson_request import view_lesson_request

import re
from django.shortcuts import render, redirect, get_object_or_404
from ..models import User, Transaction, Category, Achievement, Chart
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from ..forms import SignUpForm, LogInForm, CategoryDetailsForm, UserForm, TransactionForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from ..helpers import get_user_transactions, get_categories, get_user_balance, get_user_income, get_user_expense, get_user_budget, change_transaction_name, delete_transactions, set_achievements, get_achievements, update_achievements
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from spendingtrackers.models import Transaction
import datetime 
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime


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


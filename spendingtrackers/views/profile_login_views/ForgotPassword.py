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



def forgot_password(request):
    if request.method == 'POST':
        user_name = request.POST['email']
        pin = request.POST['pin']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$'
        if not re.match(regex, password):
            messages.add_message(request, messages.ERROR, 'Password must contain an uppercase character, a lowercase '
                                                          'character and a number')
            return render(request, 'forgot_password.html')
        user = User.objects.filter(username__exact=user_name).first()
        if not user:
            messages.add_message(request, messages.ERROR, "email does not exist!")
            return render(request, 'forgot_password.html')
        if user.pin != pin:
            messages.add_message(request, messages.ERROR, "pin error!")
            return render(request, 'forgot_password.html')
        if password != password_confirmation:
            messages.add_message(request, messages.ERROR, "The two passwords are inconsistent!")
            return render(request, 'forgot_password.html')
        user.password = make_password(password)
        user.save()
        messages.add_message(request, messages.SUCCESS, "SUCCESS!")
        return render(request, 'forgot_password.html')
    else:
        return render(request, 'forgot_password.html')

# Create your views here.
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


@login_required
def view_category(request, id):
    try:
        category = Category.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('feed')

    transactions = get_user_transactions(request.user)
    expense = category.get_expenses()
    income = category.get_income()
    balance = category.get_balance()
    currency = request.user.currency

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
            expense = category.get_expenses(from_date=from_date_obj, to_date=to_date_obj)
            income = category.get_income(from_date=from_date_obj, to_date=to_date_obj)
            balance = category.get_balance(from_date=from_date_obj, to_date=to_date_obj)

    if category.budget is not None:
        used_percentage = (category.budget - balance) / category.budget * 100
        used_percentage = round(used_percentage, 2)
    else:
        used_percentage = None
    if balance < 0:
        warning_message = "Warning: You have exceeded your budget for this category."
    elif used_percentage is not None and used_percentage >= 90:
        warning_message = "Warning: You have used {}% of your budget for this category.".format(used_percentage)
    else:
        warning_message = None

    context = {'category': category, 'transactions': transactions, 'expense': expense, 'income': income,'balance': balance, 'warning_message': warning_message, 'currency':currency}
    return render(request, 'view_category.html', context)
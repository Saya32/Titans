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
def new_transaction(request):
    try:
        if request.method == 'POST':
            form = TransactionForm(request.POST, request.FILES)
            if form.is_valid():
                category_name = form.cleaned_data['category']
                category_object = get_object_or_404(Category, user=request.user, name=category_name)

                Transaction.objects.create(
                    user=request.user,
                    title=form.cleaned_data.get('title'),
                    description=form.cleaned_data.get('description'),
                    amount=form.cleaned_data.get('amount'),
                    date_paid=form.cleaned_data.get('date_paid'),
                    time_paid=form.cleaned_data.get('time_paid'),
                    category=form.cleaned_data.get('category'),
                    receipt=form.cleaned_data.get('receipt'),
                    transaction_type=form.cleaned_data.get('transaction_type'),
                    category_fk=category_object
                )
                update_achievements(request.user)
                return redirect('feed')
            else:
                return render(request, 'new_transaction.html', {'form': form})
        else:
            form = TransactionForm()
            return render(request, 'new_transaction.html', {'form': form})
    except:
        messages.add_message(request, messages.ERROR, "Error: Category does not exist")
        return redirect('category')




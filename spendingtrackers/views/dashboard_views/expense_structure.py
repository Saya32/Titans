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



def expense_structure(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('category')
    # Extract data for graph
    labels = []
    percentlabel = []
    data = {}
    total = 0
    expense = 0
    for transaction in transactions:
        if transaction.transaction_type == "Expense":
            total += transaction.amount
    for transaction in transactions:
        labels.append(transaction.category)
        if transaction.transaction_type == "Expense":
            expense = transaction.amount
        else:
            expense = 0
        if transaction.category in data:
            data[transaction.category] = round(int(data[transaction.category]) + expense)
        else:
            data[transaction.category] = expense
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'total' : total,
        'percentlabel': percentlabel,
        'data': data,
    })

def expense_structure2(request):
    # Retrieve user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('category')
    # Extract data for graph
    labels = []
    data = {}
    expense = 0
    for transaction in transactions:
        labels.append(transaction.category)
        if transaction.transaction_type == "Expense":
            expense = transaction.amount
        else:
            expense = 0
        if transaction.category in data:
            data[transaction.category] = int(data[transaction.category]) + expense
        else:
            data[transaction.category] = expense
    # Create chart data
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


    

@login_required
def update_record(request, id):
    try:
        record = Transaction.objects.get(pk=id)
    except:
        messages.add_message(request, messages.ERROR, "Record could not be found!")
        return redirect('feed')

    
    if request.method == 'POST':
        form = TransactionForm(instance=record, data=request.POST)
        if (form.is_valid()):
            
            try:
                category_name = form.cleaned_data['category']
                category_object = get_object_or_404(Category, user=request.user, name=category_name)
            except:
                messages.add_message(request, messages.ERROR, "Category could not be found!")
                return redirect('feed')
            
            messages.add_message(request, messages.SUCCESS, "Record updated!")
            form.save()
            record = Transaction.objects.get(pk=id)
            record.category_fk = category_object
            record.save()
            return redirect('feed')
        else:
            return render(request, 'update_record.html', {'form': form, 'transaction': record})
    else:
        form = TransactionForm(instance=record)
        return render(request, 'update_record.html', {'form': form, 'transaction': record})


@login_required
def delete_record(request, id):
    if (Transaction.objects.filter(pk=id)):
        Transaction.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Record deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your record.")
        return redirect('feed')



@login_required
def edit_category_details(request, id):
    try:
        category = Category.objects.get(pk=id, user=request.user)
    except:
        messages.add_message(request, messages.ERROR, "Category could not be found!")
        return redirect('category')

    if request.method == 'POST':
        form = CategoryDetailsForm(instance=category, data=request.POST)
        if (form.is_valid()):
            change_transaction_name(request.user, category)
            messages.add_message(request, messages.SUCCESS, "Category updated!")
            form.save()
            return redirect('category')
        else:
            return render(request, 'edit_category_details.html', {'form': form, 'category': category})
    else:
        form = CategoryDetailsForm(instance=category)
        return render(request, 'edit_category_details.html', {'form': form, 'category': category})


@login_required
def delete_category(request, id):
    if (Category.objects.filter(pk=id)):
        category = Category.objects.filter(pk=id)
        delete_transactions(request.user, category)
        Category.objects.filter(pk=id).delete()
        messages.add_message(request, messages.SUCCESS, "Category deleted!")
        return redirect('feed')
    else:
        messages.add_message(request, messages.ERROR, "Sorry, an error occurred deleting your Category")
        return redirect('feed')


@login_required
def category(request):
    categories = get_categories(request.user.id)
    return render(request, 'category.html', {'categories': categories})


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

@login_required
def dashboard(request):
    balance_data = chart_balance_graph(request)
    expense_data = chart_expense_graph(request)
    income_data = chart_income_graph(request)
    expense_structure_data = expense_structure(request)
    expense_structure_data2 = expense_structure2(request)
    
    context = {
        'balance_data': balance_data,
        'expense_data': expense_data,
        'income_data': income_data,
        'expense_structure_data': expense_structure_data,
        'expense_structure_data2': expense_structure_data2,
        # other context variables
    }
    return render(request, 'dashboard.html')


@transaction.atomic        #https://docs.djangoproject.com/en/4.1/topics/db/transactions/
@login_required
def add_category_details(request):
    try:
        if request.method == 'POST':
            form = CategoryDetailsForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                messages.success(request, "Category added.")
                return redirect('category')
            else:
                messages.error(request, "Invalid form data.")
        else:
            form = CategoryDetailsForm()
        return render(request, 'add_category_details.html', {'form': form})
    except:
        with transaction.atomic(): #https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
            messages.add_message(request, messages.ERROR, "Error: Category exists")
            return redirect('category')


@login_required
def overall(request):
    transactions = get_user_transactions(request.user)
    expense = get_user_expense(request.user)
    income = get_user_income(request.user)
    balance = get_user_balance(request.user)
    budget = get_user_budget(request.user)
    currency = request.user.currency
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date_paid__range=[from_date_obj, to_date_obj])
            expense = get_user_expense(request.user, from_date=from_date_obj, to_date=to_date_obj)
            income = get_user_income(request.user, from_date=from_date_obj, to_date=to_date_obj)
            balance = get_user_balance(request.user, from_date=from_date_obj, to_date=to_date_obj)
            budget = get_user_budget(request.user, from_date=from_date_obj, to_date=to_date_obj)

    if budget:
        used_percentage = expense / budget * 100
        used_percentage = round(used_percentage, 2)
    else:
        used_percentage = None
    
    if balance < 0:
        warning_message = "Warning: You have exceeded your budget for this category."
    elif used_percentage is not None and used_percentage >= 90:
        warning_message = "Warning: You have used {}% of your budget for this category.".format(used_percentage)
    else:
        warning_message = None

    context = {'category': category, 'transactions': transactions, 'expense': expense, 'income': income, 'balance': balance, 'budget':budget,'warning_message': warning_message,'currency':currency}
    return render(request, 'overall.html', context)


@login_required
def view_achievements(request):
   achievements = get_achievements(request.user.id)
   return render(request, 'view_achievements.html', {'achievements':achievements})
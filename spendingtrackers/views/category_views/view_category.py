# Create your views here.
from django.shortcuts import render, redirect
from ..models import Category
from django.contrib.auth.decorators import login_required
from ..helpers import get_user_transactions
import matplotlib.pyplot as plt
import datetime 
from django.shortcuts import render
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
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..helpers import get_user_transactions, get_categories, get_user_balance, get_user_income, get_user_expense, get_user_budget
from spendingtrackers.models import Transaction
import datetime 
from django.shortcuts import render
from datetime import datetime


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


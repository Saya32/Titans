from .models import User, Transaction, Category
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone



def get_user_transactions(user):
    transactions = Transaction.objects.filter(user=user)
    return transactions

def get_user_income(user,from_date=None, to_date=None):
    transactions = Transaction.objects.filter(user=user)
    if from_date and to_date:
        transactions = transactions.filter(date_paid__range=[from_date, to_date])
    return sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Income')

def get_user_expense(user,from_date=None, to_date=None):
    transactions = Transaction.objects.filter(user=user)
    if from_date and to_date:
        transactions = transactions.filter(date_paid__range=[from_date, to_date])
    return sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Expense')

def get_user_budget(user,from_date=None, to_date=None):
    categories = Category.objects.filter(user=user)
    overall_budget = 0
    for category in categories:
        overall_budget= overall_budget+category.budget
    return overall_budget

def get_user_balance(user,from_date=None, to_date=None):
    if(from_date == None or to_date ==  None):
        balance =  get_user_budget(user,None,None)- get_user_expense(user,None,None)
    else:
        balance = get_user_budget(user,from_date,to_date) - get_user_expense(user,from_date,to_date)
    return balance

def change_transaction_name(user,category):
    transactions = Transaction.objects.filter(user=user)
    new_name = category.name
    for transaction in transactions:
        if  transaction.category_fk == category:
            transaction.category = new_name
            transaction.save()

def delete_transactions(user, category):
    transactions = Transaction.objects.filter(user=user)
    for transaction in transactions:
        if  transaction.category_fk == category:
            transaction.delete()


def get_all_transactions():
    transactions = Transaction.objects.filter()
    return transactions


class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

def get_categories(user):
    categories = Category.objects.filter(user=user)
    return categories



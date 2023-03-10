from .models import User, Transaction, Category, Achievement
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

def set_achievements(user):
    five_category_achievement = Achievement.objects.create(
        user = user,
        title = "Getting organised!",
        description = "Creating five new categories.",
        unlocked = False
    )

    five_transaction_achievement = Achievement.objects.create(
        user = user,
        title = "Money manager",
        description = "Recording five transactions.",
        unlocked = False
    )

def update_achievements(user):
    counter1 = 0
    categories = get_categories(user=user)
    for category in categories:
        counter1 = counter1 + 1
    if (counter1 >= 5):
        five_transaction_achievement.unlocked = True

    counter2 = 0
    transactions = get_all_transactions()
    for transaction in transactions:
        counter2 = counter2 + 1
    if (counter2 >= 5):
        five_category_achievement.unlocked = True


def get_achievements(user):
    achievements = Achievement.objects.filter(user=user)
    return achievements

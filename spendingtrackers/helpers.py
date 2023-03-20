from .models import User, Transaction, Category, Achievement
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Q
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText


def get_user_transactions(user):
    transactions = Transaction.objects.filter(user=user)
    return transactions


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


def get_user_income(user, from_date=None, to_date=None):
    transactions = Transaction.objects.filter(user=user)
    if from_date and to_date:
        transactions = transactions.filter(date_paid__range=[from_date, to_date])
    return sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Income')


def get_user_expense(user, from_date=None, to_date=None):
    transactions = Transaction.objects.filter(user=user)
    if from_date and to_date:
        transactions = transactions.filter(date_paid__range=[from_date, to_date])
    return sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Expense')


def get_user_budget(user, from_date=None, to_date=None):
    categories = Category.objects.filter(user=user)
    overall_budget = 0
    for category in categories:
        overall_budget = overall_budget + category.budget
    return overall_budget


def get_user_balance(user, from_date=None, to_date=None):
    if (from_date == None or to_date == None):
        balance = get_user_budget(user, None, None) - get_user_expense(user, None, None)
    else:
        balance = get_user_budget(user, from_date, to_date) - get_user_expense(user, from_date, to_date)
    return balance






class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

def get_categories(user):
    categories = Category.objects.filter(user=user)
    return categories

def set_achievements(user):
    new_user_achievement = Achievement.objects.create(
        user = user,
        title = "Welcome to the club",
        description = "We take budgeting serious here - welcome!",
        unlocked = True
    )

    five_category_achievement = Achievement.objects.create(
        user = user,
        title = "Getting organised!",
        description = "Creating five new categories.",
        unlocked = False
    )

    ten_category_achievement = Achievement.objects.create(
        user = user,
        title = "Category Creator",
        description = "Creating ten new categories.",
        unlocked = False
    )

    fifteen_category_achievement = Achievement.objects.create(
        user = user,
        title = "Well rounded",
        description = "Creating fifteen new categories.",
        unlocked = False
    )

    five_transaction_achievement = Achievement.objects.create(
        user = user,
        title = "Money Manager",
        description = "Recording five transactions.",
        unlocked = False
    )

    ten_transaction_achievement = Achievement.objects.create(
        user = user,
        title = "Staying on track",
        description = "Recording ten transactions.",
        unlocked = False
    )

    fifteen_transaction_achievement = Achievement.objects.create(
        user = user,
        title = "Record Keeper",
        description = "Recording fifteen transactions.",
        unlocked = False
    )

def update_achievements(user):

    category_count = Category.objects.filter(user=user).count()
    transaction_count = Transaction.objects.filter(user=user).count()
    achievements = Achievement.objects.filter(user=user)

    if category_count >= 5:
        five_category_achievement = achievements[1]
        five_category_achievement.unlocked = True
        five_category_achievement.save()

    if category_count >= 10:
        ten_category_achievement = achievements[2]
        ten_category_achievement.unlocked = True
        ten_category_achievement.save()

    if category_count >= 15:
        fifteen_category_achievement = achievements[3]
        fifteen_category_achievement.unlocked = True
        fifteen_category_achievement.save()

    if transaction_count >= 5:
        five_transaction_achievement = achievements[4]
        five_transaction_achievement.unlocked = True
        five_transaction_achievement.save()

    if transaction_count >= 10:
        ten_transaction_achievement = achievements[5]
        ten_transaction_achievement.unlocked = True
        ten_transaction_achievement.save()

    if transaction_count >= 15:
        fifteen_transaction_achievement = achievements[6]
        fifteen_transaction_achievement.unlocked = True
        fifteen_transaction_achievement.save()


def get_achievements(user):
    achievements = Achievement.objects.filter(user=user).filter(unlocked=True)
    return achievements

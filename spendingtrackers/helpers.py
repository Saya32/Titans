from .models import User, Transaction, Category
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone



def get_user_transactions(user):
    transactions = Transaction.objects.filter(user=user)
    return transactions


def get_all_transactions():
    transactions = Transaction.objects.filter()
    return transactions


class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()


def get_categories(user):
    categories = Category.objects.filter(user=user)
    return categories
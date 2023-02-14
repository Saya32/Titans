from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(AbstractUser):
    """User model used for authentication and lessons authoring."""
    username = models.EmailField(
        unique=True,
        blank=False,
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)

    class Meta(object):
        db_table = 'user'


class Transaction(models.Model):
    is_expenditure = models.BooleanField(blank=False, null=False)  # If it's false then it means Income
    title = models.CharField(blank=False, max_length=30)
    description = models.CharField(blank=True, max_length=200)
    amount = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    time_paid = models.TimeField(auto_now_add=False, blank=True, null=True)

    CATEGORY_CHOICES = [
        ('Groceries', 'Groceries'),
        ('Salary', 'Salary'),
        ('Bills', 'Bills'),
        ('Rent', 'Rent'),
        ('Gym', 'Gym'),
        ('Restaurant', 'Restaurant'),
        ('Vacation', 'Vacation'),
        ('Travel', 'Travel'),
        ('Gift', 'Gift'),
        ('Investments', 'Investments'),
        ('Savings', 'Savings'),
        ('Entertainment', 'Entertainment'),
        ('Internet', 'Internet'),
        ('Healthcare', 'Healthcare'),
        ('Lifestyle', 'Lifestyle'),
        ('Insurance', 'Insurance'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=50, blank=False, choices=CATEGORY_CHOICES)

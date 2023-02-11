from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class User(AbstractUser):
    """User model used for authentication and lessons authoring."""
    username = models.EmailField(
        unique=True,
        blank = False,
        )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    CURRENCY_CHOICES = [
        ('£','£'),
        ('$','$'),
        ('€','€'),
        ('₹','₹'),
        ('¥','¥'),
    ]
    currency = models.CharField(max_length=1, blank=False, choices=CURRENCY_CHOICES, default="£",null=True)

class Category(models.Model):
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
    category_choices = models.CharField(max_length=50, blank=False, choices=CATEGORY_CHOICES)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TRANSACTION_CHOICES = [
        ('Expense','Expense'),
        ('Income','Income'),
    ]
    transaction_type = models.CharField(max_length=10, blank=False, choices=TRANSACTION_CHOICES, default="Expense",null=True)
    title = models.CharField(blank = False, max_length=30)
    description = models.CharField(blank = True, max_length=200)
    amount = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=False, blank=True, null=True)
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
    receipt = models.ImageField(upload_to='receipts/', blank=True, null=True) #need to create receipts url pathway
    
    def __str__(self):
        return self.name

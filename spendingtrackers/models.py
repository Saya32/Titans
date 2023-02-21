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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_choices = models.CharField(max_length=50, blank=False)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=False, null=True)
    spending_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True)


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
    receipt = models.ImageField(upload_to='receipt_images', blank = True)
    
    def __str__(self):
        return self.title

    def receipt_url(self):
        if self.receipt and hasattr(self.receipt, 'url'):
            return self.receipt.url

class BiteStat(models.Model):
    exercise = models.PositiveSmallIntegerField()  # 0 to 32767
    completed = models.DateField()  # I don't care about time here
    level = models.PositiveSmallIntegerField(null=True, blank=True)
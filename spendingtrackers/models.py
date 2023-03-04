from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models import Sum

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
    name = models.CharField(max_length=50)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=False, null=True)

    def get_expenses(self, from_date=None, to_date=None):
        transactions = self.transaction_set.all()
        if from_date and to_date:
            transactions = transactions.filter(date_paid__range=[from_date, to_date])
        return sum(transaction.amount for transaction in transactions if transaction.transaction_type == 'Expense')

    def get_income(self, from_date=None, to_date=None):
        transactions = self.transaction_set.all()
        if from_date and to_date:
            transactions = transactions.filter(date_paid__range=[from_date, to_date])
        return sum(transaction.amount for transaction in transactions if transaction.transaction_type =='Income')

    def get_balance(self, from_date=None, to_date=None):
        if not from_date:
            from_date = self.start_date
        if not to_date:
            to_date = self.end_date
        expenses = self.transaction_set.filter(transaction_type='Expense',date_paid__range=[from_date, to_date]).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = self.budget - expenses
        return balance


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
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null =True)
    category = models.CharField(max_length=50, blank=False)
    receipt = models.ImageField(upload_to='images/', height_field = None, width_field = None, max_length= None, blank=True, null=True) #need to create receipts url pathway
    
    def __str__(self):
        return self.title

    def receipt_url(self):
        if self.receipt and hasattr(self.receipt, 'url'):
            return self.receipt.url

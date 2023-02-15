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

    # def create_categories(self):
    #     Category.objects.create(user=self,category_choices='Groceries', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Salary', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Bills', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Rent', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Gym', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Restaurant', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Vacation', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Travel', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Gift', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Savings', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Entertainment', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Internet', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Healthcare', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Lifestyle', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Insurance', budget=None, start_date=None, end_date=None, spending_limit=None)
    #     Category.objects.create(user=self,category_choices='Other', budget=None, start_date=None, end_date=None, spending_limit=None)
    
    # def get_category(self, category):
    #     needed_category = Category.objects.filter(category_choices=category)
    #     return needed_category

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
    category_choices = models.CharField(max_length=50, choices= CATEGORY_CHOICES, unique=True)
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
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    receipt = models.ImageField(upload_to='receipt_images', blank = True)
    
    def __str__(self):
        return self.title

    def receipt_url(self):
        if self.receipt and hasattr(self.receipt, 'url'):
            return self.receipt.url

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

    def create_categories(self):
        Category.objects.create(user=self,category_choices='Groceries', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Salary', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Bills', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Rent', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Gym', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Restaurant', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Vacation', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Travel', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Gift', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Investments', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Savings', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Entertainment', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Internet', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Healthcare', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Lifestyle', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Insurance', budget=None, start_date=None, end_date=None, spending_limit=None)
        Category.objects.create(user=self,category_choices='Other', budget=None, start_date=None, end_date=None, spending_limit=None)
    
    def get_category(self, category):
        categories = Category.objects.all().order_by('id')
        if(category=='Groceries'):
            first_post = categories[0]
            return first_post
        elif(category=='Salary'):
            second_post = categories[1]
            return second_post
        elif(category=='Bills'):
            third_post = categories[2]
            return third_post
        elif(category=='Rent'):
            fourth_post = categories[3]
            return fourth_post
        elif(category=='Gym'):
            fifth_post = categories[4]
            return fifth_post
        elif(category=='Restaurant'):
            sixth_post = categories[5]
            return sixth_post
        elif(category=='Vacation'):
            seventh_post = categories[6]
            return seventh_post
        elif(category=='Travel'):
            eight_post = categories[7]
            return eight_post
        elif(category=='Gift'):
            nine_post = categories[8]
            return nine_post
        elif(category=='Investments'):
            nine_post = categories[9]
            return nine_post
        elif(category=='Savings'):
            tenth_post = categories[10]
            return tenth_post
        elif(category=='Entertainment'):
            eleventh_post = categories[11]
            return eleventh_post
        elif(category=='Internet'):
            twelve_post = categories[12]
            return twelve_post
        elif(category=='Healthcare'):
            thirtheenth_post = categories[13]
            return thirtheenth_post
        elif(category=='Lifestyle'):
            fourteenth_post = categories[14]
            return fourteenth_post
        elif(category=='Insurance'):
            fifteenth_post = categories[15]
            return fifteenth_post
        elif(category=='Other'):
            sixteenth_post = categories[16]
            return sixteenth_post



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
    #category_fk= models.ForeignKey(Category, on_delete=models.CASCADE)
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

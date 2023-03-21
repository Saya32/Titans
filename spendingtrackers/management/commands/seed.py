from django.core.management.base import BaseCommand
from faker import Faker
from spendingtrackers.models import User, Transaction, Category
from random import randint, choice
from datetime import datetime, timedelta

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 50
    TRANSACTION_COUNT = 50
    CATEGORY_COUNT = 50
    CATEGORY_NAME = ['Salary', 'Gifts', 'Travel', 'Insurance', 'Entertainment', 'Bills', 'Rent']
   

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.create_categories()
        self.create_transactions()

    def create_users(self):
        self.create_user("John", "Doe")
        user_count = 1
        while user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            try:
                first_name = self.faker.first_name()
                last_name = self.faker.last_name()
                self.create_user(first_name, last_name)
            except:
                continue
            user_count += 1
        print("User seeding complete.")

    def create_user(self, first_name, last_name):
        username = self.email(first_name, last_name)
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
        self.user = user
    
    def create_categories(self):
        for i in range(self.CATEGORY_COUNT):
            print(f"Seeding categories {i+1}/{self.CATEGORY_COUNT}", end='\r')
            self.create_category()
        print("Categories seeding complete.")

    def create_category(self):
        name=choice(Command.CATEGORY_NAME)
        start_date = datetime.now().date() - timedelta(days=365)
        end_date = datetime.now().date() + timedelta(days=365)
        user=User.objects.order_by('?').first()
        existing_category = Category.objects.filter(user=user, name=name).first()
        if existing_category:
            return
        category = Category(
            user=user,
            name=name,
            budget=randint(1,5000),
            start_date=start_date,
            end_date=end_date,
        )
        category.save()


    def create_transactions(self):
        for user in User.objects.all():
            for category in Category.objects.filter(user=user):
                for i in range(self.TRANSACTION_COUNT):
                    print(f"Seeding transactions {i+1}/{self.TRANSACTION_COUNT}", end='\r')
                    self.create_transaction(category)
        print("Transactions seeding complete.")

    def create_transaction(self, category):
        transaction = Transaction(
            user=category.user,
            transaction_type=choice(['Expense', 'Income']),
            title=self.faker.text(max_nb_chars=30),
            amount=randint(1,5000),
            description=self.faker.text(max_nb_chars=200),
            date_paid=self.faker.date_this_year(),
            time_paid=self.faker.time(),
            category=category.name,
            receipt=None,
        )
        transaction.save()


    def email(self, first_name, last_name):
        email = f'{first_name.lower()}.{last_name.lower()}@example.org'
        return email
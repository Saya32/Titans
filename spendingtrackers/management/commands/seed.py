from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from spendingtrackers.models import User, Transaction, Category
from random import randint, random

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 50
    TRANSACTION_COUNT = 50
    CATEGORY_COUNT = 12
   

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.create_transactions()
        self.create_categories()
        self.user = User.objects.all()

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

    def create_user(self, first_name, last_name ):
        username = self.email(first_name, last_name)
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
    
    def create_transactions(self):
        for i in range(self.TRANSACTION_COUNT):
            print(f"Seeding requests {i}/{self.TRANSACTION_COUNT}", end='\r')
            self.create_transactions()
        print("Transactions seeding complete.      ")

    def create_transactions(self):
        transactions = Transaction(
            users = User.objects.get(email="john.doe@example.org"),
            transaction_type="Expense",
            title="TitleOne",
            amount=randint(1,5000),
            description="Description One",
            date_paid = "2023-12-12",
            time_paid = "20:20",
            category="Salary",
            receipt=None,
        )
        transactions.save()
    
    def create_categories(self):
        for i in range(self.CATEGORY_COUNT):
            print(f"Seeding requests {i}/{self.CATEGORY_COUNT}", end='\r')
            self.create_categories()
        print("Categories seeding complete.      ")

    def create_categories(self):
        category = Category(
            users = User.objects.get(email="john.doe@example.org"),
            name="Salary",
            budget=randint(1,5000),
            start_date = "2023-12-12",
            end_date = "2024-12-12",
        )
        category.save()

    # def get_random_user(self):
    #     index = randint(0,self.user.count()-1)
    #     return self.user[index]
    
    def email(self, first_name, last_name):
        email = f'{first_name.lower()}.{last_name.lower()}@example.org'
        return email
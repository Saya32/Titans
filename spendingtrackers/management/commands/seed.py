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
        self.create_tcategories()

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
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=Command.PASSWORD,
        )
        return user
    
    def email(self, first_name, last_name):
        email = f'{first_name.lower()}.{last_name.lower()}@example.org'
        return email
    
    def create_transactions(self):
        for i in range(self.TRANSACTION_COUNT):
            print(f"Seeding requests {i}/{self.TRANSACTION_COUNT}", end='\r')
            self.create_transactions()
        print("Request seeding complete.      ")

    def create_transactions(self):
        transactions = Transaction(
            user=self.get_random_user(),
            transaction_type='Expense',
            title="TitleOne",
            amount=40,
            description='Description One',
            date_paid = '2023-12-12',
            time_paid = '20:20',
            category='Salary',
            receipt=None,
        )
        transactions.save()
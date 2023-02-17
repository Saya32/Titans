from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from spendingtrackers.models import User

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 50
   

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()

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
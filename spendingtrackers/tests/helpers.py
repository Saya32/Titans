from django.urls import reverse
from spendingtrackers.models import Transaction, Category

class LogInTester:
    def _is_logged_in(self):
        return '_auth_user_id' in self.client.session.keys()

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url


def create_transactions(user, from_count, to_count):
    """Create unique helper testing"""
    for count in range(from_count, to_count):
        desc_text = f'Description__{count}'
        
        transaction = Transaction(
            user = user,
            title="This is a title",
            description=desc_text,
            amount=1000,
            date_paid="2023-12-12",
            time_paid="10:51",
            category= "Salary",
            receipt= "",
            transaction_type="Income"

        )
        
        transaction.save()

def create_categories(user, from_count, to_count):
    """Create unique helper testing"""
    for count in range(from_count, to_count):
        desc_text = f'Category__{count}'
        
        category = Category(
            user = user,
            name=desc_text,
            budget=1000,
            start_date="2023-12-12",
            end_date="2024-12-12"

        )
        
        category.save()

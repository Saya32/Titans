from django.urls import reverse
from spendingtrackers.models import User, Transaction

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

        transaction = Transaction(
            title="This is a title",
            description="Description of Transaction goes here",
            amount=1000,
            date_paid="2023-12-12",
            time_paid="10:51",
            category= "Salary",
            receipt="",
            transaction_type="Income"

        )
        transaction.save()

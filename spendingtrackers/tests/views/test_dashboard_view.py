from django.test import TestCase
from django.urls import reverse
from spendingtrackers.forms import TransactionForm
from spendingtrackers.models import User, Transaction
from spendingtrackers.tests.helpers import reverse_with_next, create_transactions


class DashboardViewTestCase(TestCase):
    """Test case of pending transactions view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='johndoe@example.org')
        create_transactions(self.user,0,2)
        self.transactions = Transaction.objects.filter()

    def test_dashboard_url(self):
        self.assertEqual(self.url,'/dashboard/')
    
    # def test_get_dashboard_redirects_when_not_logged_in(self):  ADD WHEN LOGIN REQUIRED IS THERE
    #      redirect_url = reverse_with_next('log_in', self.url)
    #      response = self.client.get(self.url)
    #      self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
        
 

    
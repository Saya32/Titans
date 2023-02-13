
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.forms import TransactionForm
from spendingtrackers.models import User, Transaction
from spendingtrackers.tests.helpers import reverse_with_next, create_transactions

class RecordsViewTestCase(TestCase):
    """Test case of pending transactions view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.url = reverse('records')
        self.user = User.objects.get(username='johndoe@example.org')
        create_transactions(self.user,0,2)
        self.transactions = Transaction.objects.filter()

    def test_records_url(self):
        self.assertEqual(self.url,'/records/')
    
    def test_get_records(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records.html')
    
    # def test_records_shows_student_only_their_transactions(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     other_user = User.objects.get(username='janedoe@example.org')
    #     create_transactions(other_user, 10, 20)
    #     create_transactions(self.user, 30, 40)
    #     response = self.client.get(self.url)
    #     for count in range (10,20):
    #         self.assertNotContains(response, f'Description__{count}')
    #     for count in range (30,40):
    #         self.assertContains(response, f'Description__{count}')


    # def test_get_pending_transaction_redirects_when_not_logged_in(self): //WHEN LOGIN REQUIRED IS ADDED WE CAN CHANGE THIS
    #     redirect_url = reverse_with_next('log_in', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
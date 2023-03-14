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
    
    def test_filter_transactions_by_date_range(self):
        self.client.login(username=self.user.username, password='Password123')
        create_transactions(self.user, 0, 2)
        transaction1 = Transaction.objects.first()
        transaction2 = Transaction.objects.last()
        transaction1.date_paid = '2023-02-15'
        transaction2.date_paid = '2023-02-17'
        transaction1.save()
        transaction2.save()
        response = self.client.post(self.url, {'from_date': '2023-02-14', 'to_date': '2023-02-16'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records.html')
        self.assertIn(transaction1, response.context['transactions'])
        self.assertNotIn(transaction2, response.context['transactions'])


    def test_records_redirects_when_not_logged_in(self): 
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    
    





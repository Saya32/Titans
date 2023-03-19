"""Test case of new transaction view"""
from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User, Transaction
from spendingtrackers.views import new_transaction
from spendingtrackers.forms import TransactionForm
from spendingtrackers.tests.helpers import reverse_with_next
from spendingtrackers.tests.helpers import create_transactions

class NewTransactionViewTestCase(TestCase):
    """Test case of new transaction view"""

    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
        'spendingtrackers/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='johndoe@example.org')
        self.data = {
            'title':'This is a title',
            'description':'Description of Transaction goes here',
            'amount':1000,
            'date_paid':'2023-12-12',
            'time_paid':'10:51',
            'category':'Salary',
            'receipt': '',
            'transaction_type':'expense'
        }
        self.url = reverse('new_transaction')

    def test_new_transaction_url(self):
        self.assertEqual(self.url,f'/new_transaction/')

    def test_get_new_transaction(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_transaction.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TransactionForm))
        self.assertFalse(form.is_bound)

    def test_get_new_transaction_redirects_when_not_logged_in(self):  
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_new_transaction(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_transaction.html')

    def test_unsuccessful_new_transaction(self):
        self.client.login(username=self.user.username, password="Password123")
        count_before = Transaction.objects.count()
        self.data['time'] = "not a time"
        response = self.client.post(self.url, self.data)
        count_after = Transaction.objects.count()
        self.assertEqual(count_after, count_before)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_transaction.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TransactionForm))
        self.assertTrue(form.is_bound)
    
    def test_add_existing_transaction(self):
        self.client.login(username=self.user.username, password="Password123")
        Transaction.objects.create(name=self.data['name'], user=self.user)
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        message = str(messages[0])
        self.assertIn('Error:', message)
        self.assertIn('Category exists', message)
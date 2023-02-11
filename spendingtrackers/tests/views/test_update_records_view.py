from django.test import TestCase
from django.urls import reverse
from spendingtrackers.models import User, Transaction
from spendingtrackers.forms import TransactionForm
from spendingtrackers.tests.helpers import reverse_with_next, create_transactions

class UpdateTransactionViewTestCase(TestCase):
    """Test case of edit transaction view"""
    fixtures = [
        'spendingtrackers/tests/fixtures/default_user.json',
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
            'transaction_type':'Expense'
        }
        create_transactions(self.user,1,3)
        self.transactions = Transaction.objects.filter(user = self.user)

    def test_update_record_displays_correct_page(self):
        self.client.login(username=self.user.username, password='Password123')
        transaction_url = reverse('update_record', kwargs={'id': self.transactions[0].pk})
        response = self.client.get(transaction_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_record.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TransactionForm))
        self.assertContains(response, "")

    def test_redirect_with_incorrect_transaction_id(self):
        self.client.login(username=self.user.username, password='Password123')
        transaction_url = reverse('update_record', kwargs={'id': (Transaction.objects.count()) +1})
        redirect_url = reverse('feed')
        response = self.client.get(transaction_url, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'feed.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    # def test_update_correctly_saves(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     transaction_url = reverse('update_record', kwargs={'id': self.transactions[0].pk})
    #     response = self.client.get(transaction_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'update_record.html')
    #     form = response.context['form']
    #     self.assertTrue(isinstance(form, TransactionForm))
    #     self.assertContains(response, "Expense")

    #     before_count = Transaction.objects.count()
    #     update_response = self.client.post(transaction_url, self.form_input, follow=True)
    #     after_count = Transaction.objects.count()
    #     self.assertEqual(before_count, after_count)

    #     self.assertEqual(update_response.status_code, 200)
    #     self.assertTemplateUsed(update_response, 'feed.html')
    #     messages_list = list(update_response.context['messages'])
    #     self.assertEqual(len(messages_list), 1)

    #     self.transactions = Transaction.objects.filter(user = self.user)
    #     self.assertEqual(self.transactions[0].category, 'Salary')

    # def test_update_does_not_save_if_form_is_invalid(self):
    #     self.client.login(username=self.user.username, password='Password123')
    #     transaction_url = reverse('update_record', kwargs={'id': self.transactions[0].pk})
    #     response = self.client.get(transaction_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'update_record.html')
    #     form = response.context['form']
    #     self.assertTrue(isinstance(form, TransactionForm))
    #     self.assertContains(response, "Expense")

    #     self.form_input['amount'] ='a'

    #     before_count = Transaction.objects.count()
    #     update_response = self.client.post(transaction_url, self.form_input, follow=True)
    #     after_count = Transaction.objects.count()
    #     self.assertEqual(before_count, after_count)

    #     self.assertEqual(update_response.status_code, 200)
    #     self.assertTemplateUsed(update_response, 'update_record.html')
        
    #     self.transactions = Transaction.objects.filter(user = self.user)
    #     self.assertEqual(self.transactions[0].amount, 1000)